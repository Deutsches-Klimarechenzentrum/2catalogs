#!/usr/bin/env python3
"""
Local Forge Tester - Test catalog generation locally before creating a GitHub issue.

This script simulates the GitHub forge workflow locally.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path


def create_intake_issue_body(uri: str, name: str, main_catalog_entry: str,
                              title: str, summary: str, license: str) -> str:
    """Create a simulated intake issue body."""
    body = f"""### Source URI
{uri}

### Output Catalog Name
{name}

### Desired Name in Main Catalog
{main_catalog_entry}

### Title
{title}

### Summary
{summary}

### License
{license}"""
    
    return body


def create_stac_issue_body(uri: str, collection_id: str, item_id: str = "") -> str:
    """Create a simulated STAC issue body."""
    body = f"""### Data Source URI
{uri}

### Collection ID
{collection_id}"""
    
    if item_id:
        body += f"""

### Item ID
{item_id}"""
    
    return body


def create_all_issue_body(uri: str, collection_id: str, project_id: str,
                          description: str, source_id: str = "", 
                          experiment_id: str = "", spatial_extent: str = "",
                          temporal_extent: str = "", main_catalog_entry: str = "",
                          stac_api_url: str = "") -> str:
    """Create a simulated issue body for generating all catalogs."""
    body = f"""### Data Source URI
{uri}

### Collection/Catalog ID
{collection_id}

### Project ID
{project_id}"""
    
    if source_id:
        body += f"""

### Source ID (Model)
{source_id}"""
    
    if experiment_id:
        body += f"""

### Experiment ID
{experiment_id}"""
    
    if spatial_extent:
        body += f"""

### Spatial Extent (STAC)
{spatial_extent}"""
    
    if temporal_extent:
        body += f"""

### Temporal Extent (STAC)
{temporal_extent}"""
    
    body += f"""

### Collection Description
{description}"""
    
    if main_catalog_entry:
        body += f"""

### Desired Name in Main Catalog (if public)
{main_catalog_entry}"""
    
    if stac_api_url:
        body += f"""

### STAC API URL (optional)
{stac_api_url}"""
    
    return body


def main():
    parser = argparse.ArgumentParser(
        description="Test catalog forge locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test Intake v2 generation
  python test_forge.py intake \\
    --uri https://example.com/catalog.yaml \\
    --name test-catalog \\
    --main-catalog-entry era5 \\
    --title "ERA5 Reanalysis Data" \\
    --summary "High-resolution atmospheric reanalysis dataset" \\
    --license CC-BY-4.0
  
  # Test STAC generation
  python test_forge.py stac \\
    --uri https://example.com/data.zarr \\
    --collection eerie-icon-test \\
    --item-id icon-ngc4008
  
  # Test generating all catalogs
  python test_forge.py all \\
    --uri https://example.com/data.zarr \\
    --collection eerie-icon-test \\
    --project EERIE \\
    --description "Test both catalogs" \\
    --source ICON \\
    --experiment ngc4008
        """
    )
    
    subparsers = parser.add_subparsers(dest='catalog_type', required=True)
    
    # Intake command
    intake_parser = subparsers.add_parser('intake', help='Test Intake v2 generation')
    intake_parser.add_argument('--uri', required=True, help='Source URI')
    intake_parser.add_argument('--name', required=True, help='Output catalog name')
    intake_parser.add_argument('--main-catalog-entry', required=True, help='Desired name in main catalog')
    intake_parser.add_argument('--title', required=True, help='Title')
    intake_parser.add_argument('--summary', required=True, help='Summary')
    intake_parser.add_argument('--license', required=True, help='License (e.g., CC-BY-4.0)')
    
    # STAC command
    stac_parser = subparsers.add_parser('stac', help='Test STAC generation')
    stac_parser.add_argument('--uri', required=True, help='Data source URI')
    stac_parser.add_argument('--collection', required=True, help='Collection ID')
    stac_parser.add_argument('--item-id', default='', help='Item ID')
    
    # All catalogs command
    all_parser = subparsers.add_parser('all', help='Test generation of all catalogs')
    all_parser.add_argument('--uri', required=True, help='Data source URI')
    all_parser.add_argument('--collection', required=True, help='Collection/Catalog ID')
    all_parser.add_argument('--project', required=True, help='Project ID')
    all_parser.add_argument('--description', required=True, help='Collection description')
    all_parser.add_argument('--source', default='', help='Source ID (model)')
    all_parser.add_argument('--experiment', default='', help='Experiment ID')
    all_parser.add_argument('--spatial-extent', default='', help='Spatial extent [west, south, east, north]')
    all_parser.add_argument('--temporal-extent', default='', help='Temporal extent (ISO 8601)')
    all_parser.add_argument('--main-catalog-entry', default='', help='Desired name in main catalog')
    all_parser.add_argument('--stac-api-url', default='', help='STAC API URL')
    
    args = parser.parse_args()
    
    # Create issue body
    if args.catalog_type == 'intake':
        issue_body = create_intake_issue_body(
            args.uri, args.name, args.main_catalog_entry,
            args.title, args.summary, args.license
        )
    elif args.catalog_type == 'stac':
        issue_body = create_stac_issue_body(
            args.uri, args.collection, args.item_id
        )
    else:  # all
        issue_body = create_all_issue_body(
            args.uri, args.collection, args.project,
            args.description, args.source, args.experiment,
            args.spatial_extent, args.temporal_extent,
            args.main_catalog_entry, args.stac_api_url
        )
    
    print("=" * 70)
    print("FORGE LOCAL TEST")
    print("=" * 70)
    print(f"Catalog Type: {args.catalog_type}")
    print("-" * 70)
    print("Simulated Issue Body:")
    print("-" * 70)
    print(issue_body)
    print("-" * 70)
    
    # Set environment variables
    os.environ['ISSUE_BODY'] = issue_body
    os.environ['ISSUE_NUMBER'] = 'test'
    os.environ['CATALOG_TYPE'] = args.catalog_type
    
    # Run the forge parser
    print("\nRunning forge parser...\n")
    
    # Import and run the parser
    if not 'forge_output' in sys.path:
        sys.path.insert(0, str(Path(__file__).parent.parent / '.gitlab' / 'scripts'))
    
    try:
        import forge_parser
        forge_parser.main()
    except SystemExit as e:
        if e.code == 0:
            print("\n" + "=" * 70)
            print("✅ FORGE TEST COMPLETED SUCCESSFULLY")
            print("=" * 70)
            print("\nOutput available in: forge_output/")
            print("\nTo view the generated catalog:")
            print("  ls -lh forge_output/")
            print("  cat forge_output/info.txt")
        else:
            print("\n" + "=" * 70)
            print("❌ FORGE TEST FAILED")
            print("=" * 70)
            if Path('forge_output/error.log').exists():
                print("\nError log:")
                print(Path('forge_output/error.log').read_text())
        sys.exit(e.code)


if __name__ == '__main__':
    main()
