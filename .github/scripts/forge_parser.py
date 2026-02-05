#!/usr/bin/env python3
"""
Forge Parser - Extract inputs from GitHub issues and run catalog generators.

This script is called by the GitHub Actions workflow to parse issue bodies
and execute the appropriate catalog generation tool.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def parse_issue_body(body: str) -> Dict[str, str]:
    """
    Parse the GitHub issue body and extract form fields.
    
    GitHub issue forms create a specific format like:
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
    
    # Build the command
    cmd = [
        sys.executable,  # Use same Python interpreter
        '-m', 'generators.intake.v2.tointake2',
        source_uri,
        '--out', str(output_dir / f'{output_name}.yaml')
    ]
    
    # Add source type if not auto-detect
    if source_type != 'Auto-detect':
        type_map = {
            'Intake v1 YAML Catalog': 'yaml',
            'Zarr Store': 'zarr',
            'Reference Parquet': 'parquet'
        }
        if source_type in type_map:
            # Note: tointake2 auto-detects, but we log it
            logger.info(f"Source type specified: {type_map[source_type]}")
    
    # Add additional options
    if additional_options:
        for opt in additional_options.split('\n'):
            opt = opt.strip()
            if opt and not opt.startswith('#'):
                # Handle options that might have spaces
                if opt.startswith('--'):
                    cmd.append(opt)
                else:
                    cmd.extend(opt.split())
    
    # Write info
    info_path = output_dir / 'info.txt'
    with open(info_path, 'w') as f:
        f.write(f"Catalog Type: Intake v2\n")
        f.write(f"Source URI: {source_uri}\n")
        f.write(f"Output Name: {output_name}.yaml\n")
        f.write(f"Source Type: {source_type}\n")
        if fields.get('Description'):
            f.write(f"Description: {fields['Description']}\n")
        f.write(f"\nCommand executed:\n{' '.join(cmd)}\n")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=600  # 10 minute timeout
        )
        
        # Save output logs
        with open(output_dir / 'stdout.log', 'w') as f:
            f.write(result.stdout)
        with open(output_dir / 'stderr.log', 'w') as f:
            f.write(result.stderr)
        
        return 0
    
    except subprocess.CalledProcessError as e:
        # Save error logs
        with open(output_dir / 'error.log', 'w') as f:
            f.write(f"Command failed with exit code {e.returncode}\n\n")
            f.write(f"STDOUT:\n{e.stdout}\n\n")
            f.write(f"STDERR:\n{e.stderr}\n")
        return e.returncode
    
    except subprocess.TimeoutExpired:
        with open(output_dir / 'error.log', 'w') as f:
            f.write("Command timed out after 10 minutes\n")
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
    # Get environment variables
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
            exit_code = run_intake_forge(fields, output_dir)
        elif catalog_type == 'stac':
            exit_code = run_stac_forge(fields, output_dir)
        elif catalog_type == 'all':
            print("Running both Intake and STAC forge...")
            # Run intake first
            print("\n=== Generating Intake v2 Catalog ===")
            intake_exit = run_intake_forge(fields, output_dir)
            if intake_exit != 0:
                print("Warning: Intake generation failed")
            
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
