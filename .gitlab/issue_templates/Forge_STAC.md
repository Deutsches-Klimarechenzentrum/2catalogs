---
name: Forge STAC Catalog
about: Request generation of a STAC catalog/collection from data
title: "[Forge-STAC] "
labels: ["forge-stac", "catalog-generation"]
---

<!-- 
This issue will trigger the GitLab CI pipeline to automatically generate a STAC catalog.
To manually trigger: Go to CI/CD > Pipelines > Run Pipeline > Select "forge:stac" job
-->

## Data Source Information

### Data Source URI
<!-- Provide the URI to the data source -->
<!-- Example: https://example.com/data.zarr or s3://bucket/path/to/data -->


### Collection ID
<!-- Unique identifier for the STAC collection -->
<!-- Use lowercase with hyphens, e.g., my-satellite-data -->


### Project ID
<!-- Short project identifier or code (e.g., NASA, ESA, NOAA) -->


## Collection Metadata

### Collection Title
<!-- Human-readable title for the collection -->


### Collection Description
<!-- Detailed description of the collection and its contents -->



### License
<!-- Specify the data license -->
<!-- Example: CC-BY-4.0, MIT, proprietary, etc. -->


### Keywords
<!-- Comma-separated list of relevant keywords -->


## Spatial and Temporal Coverage

### Geographic Bounding Box
<!-- Optional: Specify the bounding box coordinates -->

- **West Longitude**: 
- **South Latitude**: 
- **East Longitude**: 
- **North Latitude**: 

### Temporal Extent
<!-- Optional: Specify the temporal coverage -->

- **Start Date**: <!-- YYYY-MM-DD -->
- **End Date**: <!-- YYYY-MM-DD or "ongoing" -->

### Coordinate Reference System
<!-- Default: EPSG:4326 (WGS84) -->


## Data Information

### Data Format
<!-- Select the primary data format -->

- [ ] Zarr
- [ ] NetCDF
- [ ] COG (Cloud Optimized GeoTIFF)
- [ ] GeoTIFF
- [ ] HDF5
- [ ] Parquet
- [ ] CSV
- [ ] Other:

### Storage Location
<!-- Where is the data stored? -->

- [ ] Cloud Storage (S3, GCS, Azure)
- [ ] HTTP/HTTPS Server
- [ ] On-premises
- [ ] Local filesystem

**Storage URL pattern:**


### Data Variables
<!-- List the main variables/bands in the dataset -->



### Resolution
<!-- Spatial and/or temporal resolution -->

- **Spatial**: <!-- e.g., 10m, 0.25 degrees -->
- **Temporal**: <!-- e.g., daily, monthly, yearly -->

## Asset Configuration

### Asset Types
<!-- Check all asset types that should be included -->

- [ ] Data (primary data files)
- [ ] Metadata (sidecar metadata files)
- [ ] Thumbnail (preview images)
- [ ] Documentation
- [ ] Other:

### Access Configuration
<!-- Configure data access parameters -->

**Base URL for assets:** <!-- <ASSET_BASE_URL> -->

**Access protocol:**
- [ ] HTTPS
- [ ] S3
- [ ] Azure Blob
- [ ] Google Cloud Storage
- [ ] Other:

**Authentication required:**
- [ ] Yes
- [ ] No

## Additional Configuration

### Provider Information
<!-- Organization or individual providing the data -->

- **Provider Name**: 
- **Provider URL**: 
- **Role**: <!-- e.g., producer, licensor, processor -->

### Contact Information
<!-- Optional: Contact details for data inquiries -->

- **Contact Name**: 
- **Contact Email**: 
- **Contact URL**: 

### STAC Extensions
<!-- Select any STAC extensions that should be used -->

- [ ] datacube
- [ ] eo (Electro-Optical)
- [ ] sar (Synthetic Aperture Radar)
- [ ] projection
- [ ] scientific
- [ ] version
- [ ] Other:

## API Integration

### STAC API Endpoint
<!-- If uploading to a STAC API, provide the endpoint -->
<!-- Placeholder: <STAC_API_URL> -->


### API Authentication
<!-- Configuration for STAC API access -->

- [ ] No authentication
- [ ] API Key (configure in CI/CD variables as STAC_API_KEY)
- [ ] OAuth2 (configure tokens in CI/CD variables)
- [ ] Other:

## Testing and Validation

### Validation Requirements
<!-- How should we validate the generated STAC catalog? -->

- [ ] STAC validation (stac-validator)
- [ ] Manual review
- [ ] Test with specific STAC tools (specify below)

**Tools to test with:**


### Test Queries
<!-- Example queries that should work with this catalog -->



## Additional Notes
<!-- Any other information that would be helpful -->



---

## For Pipeline Variables (Manual Trigger)

If triggering manually via CI/CD pipeline:

```bash
# Set these variables when running the pipeline:
CATALOG_TYPE="stac"
ISSUE_NUMBER="<THIS_ISSUE_NUMBER>"
ISSUE_BODY="<PASTE_THIS_ISSUE_CONTENT>"
# Optional API configuration:
STAC_API_URL="<YOUR_STAC_API_URL>"
STAC_API_KEY="<YOUR_API_KEY>"  # Set as protected variable in CI/CD settings
```

---
/label ~"forge-stac" ~"catalog-generation" ~"automation"
