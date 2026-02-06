#!/usr/bin/env python3
"""
Forge Parser - Extract inputs from GitLab/GitHub issues and run catalog generators.

This script is called by the GitLab CI/CD or GitHub Actions workflow to parse issue bodies
and execute the appropriate catalog generation tool.
"""

import json
import logging
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# Import intake and tointake2 functions
import intake
from generators.intake.v2.tointake2 import convert_to_intake2, setup_logging as setup_tointake2_logging


def parse_issue_body(body: str) -> Dict[str, str]:
    """
    Parse the GitLab/GitHub issue body and extract form fields.
    
    Both platforms create a similar format:
    ### Field Label
    field value
    """
    fields = {}
    lines = body.split('\n')
    current_field = None
    current_value = []
    
    for line in lines:
        # Check if this is a field header (starts with ###)
        if line.startswith('###'):
            # Save previous field if exists
            if current_field:
                fields[current_field] = '\n'.join(current_value).strip()
            
            # Start new field
            current_field = line.replace('###', '').strip()
            current_value = []
        elif current_field:
            # Add to current field value
            if line.strip() and not line.startswith('_No response_'):
                current_value.append(line.strip())
    
    # Save last field
    if current_field:
        fields[current_field] = '\n'.join(current_value).strip()
    
    return fields


def load_main_catalog() -> Dict:
    """Load the main community catalog."""
    catalog_path = Path('catalog/main.yaml')
    if not catalog_path.exists():
        return {
            'metadata': {
                'version': 1,
                'name': '2catalogs Community Catalog',
                'description': 'Publicly contributed Intake v2 catalogs',
                'created': datetime.now().date().isoformat(),
                'last_updated': datetime.now().date().isoformat()
            },
            'sources': {}
        }
    
    with open(catalog_path, 'r') as f:
        return yaml.safe_load(f)


def check_duplicate(catalog_name: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a catalog entry already exists in the main catalog.
    
    Returns:
        Tuple of (is_duplicate, existing_source_uri)
    """
    try:
        main_catalog = load_main_catalog()
        sources = main_catalog.get('sources', {})
        
        if catalog_name in sources:
            existing_uri = sources[catalog_name].get('args', {}).get('urlpath', 'unknown')
            return True, existing_uri
        
        return False, None
    except Exception as e:
        print(f"Warning: Could not check for duplicates: {e}")
        return False, None


def add_to_main_catalog(catalog_name: str, catalog_path: Path, fields: Dict[str, str], issue_number: str) -> bool:
    """
    Add a new catalog entry to the main community catalog.
    
    Returns:
        True if successfully added, False otherwise
    """
    try:
        main_catalog = load_main_catalog()
        
        # Check if marked as public
        visibility = fields.get('Visibility', '')
        is_public = 'Make this catalog publicly accessible' in visibility
        
        if not is_public:
            print(f"Catalog '{catalog_name}' is not marked as public, skipping addition to main catalog")
            return False
        
        # Check for duplicate
        is_dup, existing_uri = check_duplicate(catalog_name)
        if is_dup:
            print(f"⚠️  Duplicate found: '{catalog_name}' already exists in main catalog")
            print(f"   Existing URI: {existing_uri}")
            return False
        
        # Read the generated catalog
        if not catalog_path.exists():
            print(f"Generated catalog not found at {catalog_path}")
            return False
        
        # Use intake to load the catalog
        generated_catalog = intake.open_catalog(str(catalog_path))
        
        # Extract source info from generated catalog
        source_uri = fields.get('Source URI', '')
        description = fields.get('Description', 'No description provided')
        
        # Add entry to main catalog
        main_catalog['sources'][catalog_name] = {
            'driver': 'intake.catalog.local.YAMLFileCatalog',
            'description': description,
            'args': {
                'path': f'{{{{ CATALOG_DIR }}}}/generated/{catalog_name}.yaml'
            },
            'metadata': {
                'source_uri': source_uri,
                'added': datetime.now().date().isoformat(),
                'issue': issue_number,
                'project': fields.get('Project ID', 'unknown')
            }
        }
        
        # Update metadata
        main_catalog['metadata']['last_updated'] = datetime.now().date().isoformat()
        
        # Save updated catalog
        catalog_dir = Path('catalog')
        catalog_dir.mkdir(exist_ok=True)
        
        with open(catalog_dir / 'main.yaml', 'w') as f:
            yaml.dump(main_catalog, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Added '{catalog_name}' to main catalog")
        return True
        
    except Exception as e:
        print(f"Error adding to main catalog: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_output_dir():
    """Create the forge output directory."""
    output_dir = Path('forge_output')
    output_dir.mkdir(exist_ok=True, parents=True)
    return output_dir


def run_intake_forge(fields: Dict[str, str], output_dir: Path) -> int:
    """
    Run the intake catalog generation.
    
    Args:
        fields: Parsed fields from the issue
        output_dir: Directory to save outputs
    
    Returns:
        Exit code (0 for success)
    """
    source_uri = fields.get('Source URI', '').strip()
    output_name = fields.get('Output Catalog Name', 'catalog').strip()
    source_type = fields.get('Source Type', 'Auto-detect').strip()
    additional_options = fields.get('Additional Options', '').strip()
    
    if not source_uri:
        raise ValueError("Source URI is required")
    
    output_path = str(output_dir / f'{output_name}.yaml')
    
    # Log source type if specified
    if source_type != 'Auto-detect':
        type_map = {
            'Intake v1 YAML Catalog': 'yaml',
            'Zarr Store': 'zarr',
            'Reference Parquet': 'parquet'
        }
        if source_type in type_map:
            print(f"Source type specified: {type_map[source_type]}")
    
    # Write info
    info_path = output_dir / 'info.txt'
    with open(info_path, 'w') as f:
        f.write(f"Catalog Type: Intake v2\n")
        f.write(f"Source URI: {source_uri}\n")
        f.write(f"Output Name: {output_name}.yaml\n")
        f.write(f"Source Type: {source_type}\n")
        if fields.get('Description'):
            f.write(f"Description: {fields['Description']}\n")
        if additional_options:
            f.write(f"Additional Options: {additional_options}\n")
    
    print(f"Converting {source_uri} to Intake v2 catalog: {output_path}")
    
    try:
        # Call convert_to_intake2 directly instead of subprocess
        convert_to_intake2([source_uri], output_path)
        
        print(f"✓ Successfully created catalog: {output_path}")
        return 0
    
    except Exception as e:
        # Save error logs
        error_msg = f"Error converting catalog: {str(e)}\n"
        with open(output_dir / 'error.log', 'w') as f:
            f.write(error_msg)
            import traceback
            f.write(traceback.format_exc())
        
        print(f"✗ Error: {e}")
        return 1


def run_stac_forge(fields: Dict[str, str], output_dir: Path) -> int:
    """
    Run the STAC catalog generation.
    
    Args:
        fields: Parsed fields from the issue
        output_dir: Directory to save outputs
    
    Returns:
        Exit code (0 for success)
    """
    source_uri = fields.get('Data Source URI', '').strip()
    collection_id = fields.get('Collection ID', '').strip()
    project_id = fields.get('Project ID', '').strip()
    description = fields.get('Collection Description', '').strip()
    
    if not all([source_uri, collection_id, project_id, description]):
        raise ValueError("Source URI, Collection ID, Project ID, and Description are required")
    
    # Write info
    info_path = output_dir / 'info.txt'
    with open(info_path, 'w') as f:
        f.write(f"Catalog Type: STAC\n")
        f.write(f"Data Source: {source_uri}\n")
        f.write(f"Collection ID: {collection_id}\n")
        f.write(f"Project ID: {project_id}\n")
        f.write(f"Description: {description}\n")
        if fields.get('Source ID (Model)'):
            f.write(f"Source ID: {fields['Source ID (Model)']}\n")
        if fields.get('Experiment ID'):
            f.write(f"Experiment ID: {fields['Experiment ID']}\n")
    
    # For now, create a placeholder for STAC generation
    # This would be replaced with actual STAC generation logic
    print("STAC generation requested")
    print(f"Collection ID: {collection_id}")
    print(f"Project ID: {project_id}")
    print(f"Source URI: {source_uri}")
    
    # Create a placeholder STAC catalog
    stac_json = {
        "stacVersion": "1.0.0",
        "type": "Collection",
        "id": collection_id,
        "description": description,
        "license": "proprietary",
        "extent": {
            "spatial": {"bbox": [[-180, -90, 180, 90]]},
            "temporal": {"interval": [[None, None]]}
        },
        "links": []
    }
    
    with open(output_dir / f"{collection_id}.json", 'w') as f:
        json.dump(stac_json, f, indent=2)
    
    with open(output_dir / 'README.md', 'w') as f:
        f.write(f"# STAC Collection: {collection_id}\n\n")
        f.write(f"**Project:** {project_id}\n\n")
        f.write(f"**Description:** {description}\n\n")
        f.write(f"**Source:** {source_uri}\n\n")
        f.write("## Note\n\n")
        f.write("This is a generated STAC collection. ")
        f.write("Full STAC generation with item creation is coming soon.\n")
    
    return 0


def main():
    """Main entry point."""
    # Setup logging for tointake2
    setup_tointake2_logging(logging.INFO)
    
    # Get environment variables (works for both GitLab and GitHub)
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')
    catalog_type = os.environ.get('CATALOG_TYPE', 'intake')
    
    print(f"Processing issue #{issue_number}")
    print(f"Catalog type: {catalog_type}")
    
    # Parse the issue body
    try:
        fields = parse_issue_body(issue_body)
        print(f"Parsed {len(fields)} fields from issue")
        
        # Debug: print parsed fields
        for key, value in fields.items():
            print(f"  {key}: {value[:100]}..." if len(value) > 100 else f"  {key}: {value}")
        
    except Exception as e:
        print(f"Error parsing issue body: {e}")
        sys.exit(1)
    
    # Create output directory
    try:
        output_dir = create_output_dir()
        print(f"Output directory: {output_dir}")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)
    
    # Run the appropriate forge
    try:
        if catalog_type == 'intake':
            # Check for duplicates before running
            catalog_name = fields.get('Output Catalog Name', 'catalog').strip()
            is_dup, existing_uri = check_duplicate(catalog_name)
            if is_dup:
                warning_msg = (
                    f"⚠️  **Duplicate Entry Warning**\n\n"
                    f"A catalog named `{catalog_name}` already exists in the main community catalog.\n\n"
                    f"**Existing source:** {existing_uri}\n\n"
                    f"Your catalog will still be generated and available as an artifact, "
                    f"but it will **not** be added to the main community catalog.\n\n"
                    f"If you want to add it, please:\n"
                    f"1. Choose a different catalog name\n"
                    f"2. Create a new issue with the updated name"
                )
                # Write warning to file for workflow to display
                with open(output_dir / 'duplicate_warning.txt', 'w') as f:
                    f.write(warning_msg)
                print(warning_msg)
            
            exit_code = run_intake_forge(fields, output_dir)
            
            # Add to main catalog if successful and not duplicate
            if exit_code == 0 and not is_dup:
                catalog_path = output_dir / f'{catalog_name}.yaml'
                added = add_to_main_catalog(catalog_name, catalog_path, fields, issue_number)
                if added:
                    with open(output_dir / 'added_to_main.txt', 'w') as f:
                        f.write(f"✓ Added to main community catalog as '{catalog_name}'")
                        
        elif catalog_type == 'stac':
            exit_code = run_stac_forge(fields, output_dir)
        elif catalog_type == 'all':
            print("Running both Intake and STAC forge...")
            # Check for duplicates for intake
            catalog_name = fields.get('Collection/Catalog ID', 'catalog').strip()
            is_dup, existing_uri = check_duplicate(catalog_name)
            if is_dup:
                warning_msg = (
                    f"⚠️  **Duplicate Entry Warning**\n\n"
                    f"A catalog named `{catalog_name}` already exists.\n\n"
                    f"**Existing source:** {existing_uri}\n\n"
                    f"Your catalogs will still be generated but not added to the main catalog."
                )
                with open(output_dir / 'duplicate_warning.txt', 'w') as f:
                    f.write(warning_msg)
                print(warning_msg)
            
            # Run intake first
            print("\n=== Generating Intake v2 Catalog ===")
            intake_exit = run_intake_forge(fields, output_dir)
            if intake_exit != 0:
                print("Warning: Intake generation failed")
            elif not is_dup:
                catalog_path = output_dir / f'{catalog_name}.yaml'
                add_to_main_catalog(catalog_name, catalog_path, fields, issue_number)
            
            # Then run STAC
            print("\n=== Generating STAC Catalog ===")
            stac_exit = run_stac_forge(fields, output_dir)
            if stac_exit != 0:
                print("Warning: STAC generation failed")
            
            # Return 0 if at least one succeeded
            exit_code = 0 if (intake_exit == 0 or stac_exit == 0) else 1
        else:
            print(f"Unknown catalog type: {catalog_type}")
            sys.exit(1)
        
        sys.exit(exit_code)
    
    except Exception as e:
        error_path = output_dir / 'error.log'
        with open(error_path, 'w') as f:
            f.write(f"Error in forge parser: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
        
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
