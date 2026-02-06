---
name: Forge All Catalogs
about: Request generation of both Intake and STAC catalogs
title: "[Forge-All] "
labels: ["forge-intake", "forge-stac", "catalog-generation"]
---

<!-- 
This issue will trigger the GitLab CI pipeline to automatically generate both Intake and STAC catalogs.
To manually trigger: Go to CI/CD > Pipelines > Run Pipeline > Select "forge:all" job
-->

## Data Source Information

### Primary Data Source URI
<!-- Provide the URI to the primary data source -->


### Output Name/ID
<!-- Base name/ID for both catalog types -->


### Collection Title
<!-- Human-readable title -->


### Description
<!-- Detailed description of the data -->



## Intake Catalog Configuration

### Intake Source Type
<!-- Type of source for Intake catalog -->

- [ ] Intake v1 YAML Catalog
- [ ] Local Data Files
- [ ] Remote Data (HTTP/S3)
- [ ] Other:

### Intake-specific Notes
<!-- Any Intake-specific configuration -->



## STAC Catalog Configuration

### STAC Collection ID
<!-- Unique identifier for STAC collection -->


### Project ID
<!-- Project or organization code -->


### License
<!-- Data license (e.g., CC-BY-4.0) -->


### STAC-specific Notes
<!-- Any STAC-specific configuration -->



## Common Metadata

### Geographic Coverage

- **Bounding Box (W, S, E, N)**: 
- **CRS**: <!-- Default: EPSG:4326 -->

### Temporal Coverage

- **Start Date**: <!-- YYYY-MM-DD -->
- **End Date**: <!-- YYYY-MM-DD or ongoing -->

### Data Format
<!-- Select the primary format -->

- [ ] Zarr
- [ ] NetCDF
- [ ] GeoTIFF/COG
- [ ] HDF5
- [ ] CSV/Parquet
- [ ] Other:

### Keywords/Tags
<!-- Comma-separated keywords -->


### Resolution
- **Spatial**: 
- **Temporal**: 

## Access Configuration

### Storage Location
<!-- Where is the data stored? -->

- [ ] Public (no auth)
- [ ] Private (auth required)

**Base URL Pattern**: <!-- <ASSET_BASE_URL> -->

**Access Protocol**:
- [ ] HTTPS
- [ ] S3
- [ ] Azure
- [ ] GCS
- [ ] Other:

### Authentication
<!-- If required, how should it be configured? -->



## Provider Information

- **Provider Name**: 
- **Provider URL**: 
- **Contact Email**: 

## API Integration

### STAC API Endpoint
<!-- Optional: STAC API to publish to -->
<!-- Placeholder: <STAC_API_URL> -->


### API Configuration
<!-- API authentication and configuration details -->



## Testing Requirements

### Validation Steps
<!-- How should we validate the generated catalogs? -->

- [ ] Validate Intake catalog loads correctly
- [ ] Validate STAC catalog with stac-validator
- [ ] Test data access through both catalogs
- [ ] Manual review

### Test Queries/Access Patterns
<!-- Example queries or access patterns to test -->



## Additional Configuration

### Special Requirements
<!-- Any special processing or configuration needs -->



### Dependencies
<!-- List any dependencies on other catalogs or data -->



## Additional Notes
<!-- Any other relevant information -->



---

## For Pipeline Variables (Manual Trigger)

If triggering manually via CI/CD pipeline:

```bash
# Set these variables when running the pipeline:
CATALOG_TYPE="all"
ISSUE_NUMBER="<THIS_ISSUE_NUMBER>"
ISSUE_BODY="<PASTE_THIS_ISSUE_CONTENT>"

# Optional API configuration:
STAC_API_URL="<YOUR_STAC_API_URL>"
STAC_API_KEY="<YOUR_API_KEY>"  # Set as protected variable
API_BASE_URL="<YOUR_API_BASE_URL>"
```

## Generated Outputs

This will generate:
1. **Intake Catalog**: YAML file in `catalog/` directory
2. **STAC Collection**: JSON files in `catalog/stac/` directory
3. **Documentation**: Info and metadata files in `forge_output/`

Both catalogs will reference the same underlying data source but provide different access methods.

---
/label ~"forge-intake" ~"forge-stac" ~"catalog-generation" ~"automation"
