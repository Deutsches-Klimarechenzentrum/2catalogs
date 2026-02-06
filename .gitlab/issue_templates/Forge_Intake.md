---
name: Forge Intake Catalog
about: Request generation of an Intake catalog from existing sources
title: "[Forge-Intake] "
labels: ["forge-intake", "catalog-generation"]
---

<!-- 
This issue will trigger the GitLab CI pipeline to automatically generate an Intake catalog.
To manually trigger: Go to CI/CD > Pipelines > Run Pipeline > Select "forge:intake" job
-->

## Source Information

### Source URI
<!-- Provide the URI to the source catalog or data -->
<!-- Example: https://example.com/catalog.yaml or file:///path/to/catalog.yaml -->


### Output Catalog Name
<!-- The name for the generated catalog entry -->
<!-- Use lowercase with hyphens, e.g., my-data-catalog -->


### Source Type
<!-- Select the type of source you're converting -->

- [ ] Intake v1 YAML Catalog
- [ ] Intake v1 JSON Catalog
- [ ] CSV/TSV File List
- [ ] Directory of Files
- [ ] Other (specify below)

**If Other, specify:**


### Description
<!-- Provide a description of the catalog and its contents -->



## Additional Configuration

### Access Requirements
<!-- Does this data require authentication or special access? -->

- [ ] Public (no authentication required)
- [ ] Authentication required (will be configured separately)

**If authentication required, specify method:**


### Data Format
<!-- What format is the underlying data? -->

- [ ] NetCDF
- [ ] Zarr
- [ ] HDF5
- [ ] CSV
- [ ] Parquet
- [ ] GeoTIFF
- [ ] Other:

### Geographic Coverage
<!-- Optional: Describe the geographic coverage -->


### Temporal Coverage
<!-- Optional: Describe the temporal coverage -->


### Keywords/Tags
<!-- Optional: Add relevant keywords (comma-separated) -->


## Testing Instructions
<!-- How should we verify the generated catalog works correctly? -->



## Additional Notes
<!-- Any other information that would be helpful -->



---

## For Pipeline Variables (Manual Trigger)

If triggering manually via CI/CD pipeline:

```bash
# Set these variables when running the pipeline:
CATALOG_TYPE="intake"
ISSUE_NUMBER="<THIS_ISSUE_NUMBER>"
ISSUE_BODY="<PASTE_THIS_ISSUE_CONTENT>"
```

---
/label ~"forge-intake" ~"catalog-generation" ~"automation"
