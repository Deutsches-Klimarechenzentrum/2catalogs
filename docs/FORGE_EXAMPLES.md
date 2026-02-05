# Forge Examples

This document provides example scenarios for using the catalog forge.

## Example 1: Convert Public Intake v1 Catalog

**Scenario:** You have a public Intake v1 catalog that you want to convert to Intake v2.

**Steps:**

1. Create a new issue using the "Generate Intake v2 Catalog" template
2. Fill in:
   - **Source URI:** `https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml`
   - **Output Catalog Name:** `hackathon-intake-v2`
   - **Source Type:** `Intake v1 YAML Catalog`
   - **Description:** `Digital Earth's Global Hackathon catalog converted to Intake v2`

3. Submit the issue
4. Wait for the forge to complete (~2-5 minutes)
5. Download the artifact from the Actions tab

**Expected Output:**
- `hackathon-intake-v2.yaml` - The converted Intake v2 catalog
- `info.txt` - Generation metadata
- `stdout.log` - Generator output
- `stderr.log` - Any warnings

## Example 2: Generate STAC Collection from Zarr

**Scenario:** You have EERIE model data in Zarr format that needs a STAC collection.

**Steps:**

1. Create a new issue using the "Generate STAC Catalog" template
2. Fill in:
   - **Data Source URI:** `https://s3.dkrz.de/my-bucket/eerie/icon-ngc4008.zarr`
   - **Collection ID:** `eerie-icon-ngc4008`
   - **Project ID:** `EERIE`
   - **Source ID:** `ICON`
   - **Experiment ID:** `ngc4008`
   - **Description:** `High-resolution ICON atmospheric model output from the EERIE project`
   - Check "Use EERIE Cloud template"

3. Submit the issue
4. Wait for the forge to complete
5. Download the STAC collection JSON

**Expected Output:**
- `eerie-icon-ngc4008.json` - STAC Collection
- `README.md` - Collection documentation
- `info.txt` - Generation metadata

## Example 3: Local Test Before Creating Issue

**Scenario:** You want to test the forge locally before creating a GitHub issue.

### Test Intake Conversion

```bash
# Install dependencies
pip install -e ".[intake]"

# Test with a remote catalog
python tests/test_forge.py intake \
  --uri "https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml" \
  --name "test-catalog" \
  --source-type "Intake v1 YAML Catalog" \
  --description "Test conversion"

# Check output
ls -lh forge_output/
cat forge_output/info.txt
```

### Test STAC Generation

```bash
# Install dependencies
pip install -e ".[stac]"

# Test STAC generation
python tests/test_forge.py stac \
  --uri "https://example.com/data.zarr" \
  --collection "test-collection" \
  --project "EERIE" \
  --source "ICON" \
  --experiment "test" \
  --description "Test STAC collection for validation"

# Check output
ls -lh forge_output/
cat forge_output/test-collection.json
```

## Example 4: Batch Conversion

**Scenario:** You need to convert multiple catalogs.

**Strategy:**

1. Create one issue per catalog
2. Use consistent naming: `[Forge-Intake] Dataset Name`
3. Label all issues with an additional custom label like `batch-2024-02`
4. Issues will process in parallel (up to GitHub's concurrency limits)

**Monitoring:**

```bash
# Using GitHub CLI
gh issue list --label "forge-intake,batch-2024-02"

# Check status
gh issue list --label "forge-complete,batch-2024-02"
gh issue list --label "forge-failed,batch-2024-02"
```

## Example 5: Custom Options

**Scenario:** You need specific tointake2 options.

**Additional Options Field:**
```
--log-level DEBUG
```

This will be added to the command line execution.

## Example 6: Reference Parquet (Kerchunk)

**Scenario:** You have Kerchunk reference files in Parquet format.

**Steps:**

1. Use "Generate Intake v2 Catalog" template
2. Fill in:
   - **Source URI:** `reference::s3://bucket/references/dataset.parq`
   - **Output Catalog Name:** `kerchunk-catalog`
   - **Source Type:** `Reference Parquet`
   - **Description:** `Kerchunk references for large dataset`

## Common Patterns

### Pattern: Testing with Small Data First

Always test with a subset or small catalog first:

1. Create issue with small test dataset
2. Verify output format and structure
3. Then process full dataset

### Pattern: Adding Metadata

Use the Description field extensively:
- Dataset provenance
- Processing notes
- Contact information
- License information

### Pattern: Issue as Documentation

The issue becomes documentation:
- Keep all metadata in the issue
- Link to related issues
- Tag with project labels
- Close when no longer needed

## Troubleshooting Examples

### Problem: "Source URI not accessible"

**Solution:**
- Verify URL is publicly accessible
- Check for typos in URL
- Test URL in browser first
- Ensure no authentication required

### Problem: "Timeout after 10 minutes"

**Solution:**
- Split large catalogs into smaller chunks
- Use reference:: format for large datasets
- Contact maintainers for timeout increase

### Problem: "Invalid YAML format"

**Solution:**
- Check the source catalog syntax
- Validate YAML online first
- Look for special characters in strings
- Ensure proper indentation

## Advanced: Extending the Forge

Want to add a new catalog type? See [SETUP_GUIDE.md](../SETUP_GUIDE.md) for development instructions.

### Add New Generator

1. Create new issue template in `.github/ISSUE_TEMPLATE/`
2. Add handler function in `.github/scripts/forge_parser.py`
3. Add corresponding label
4. Update workflow to handle new label
5. Test locally with `tests/test_forge.py`

### Example: Adding NetCDF Support

```python
def run_netcdf_forge(fields: Dict[str, str], output_dir: Path) -> int:
    """Run NetCDF to catalog generation."""
    # Implementation here
    pass
```

Then update `main()` to call it based on label.
