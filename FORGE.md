# Catalog Forge - Automated Catalog Generation

The 2catalogs project includes a "forge" mechanism that automatically generates catalogs through GitHub Issues. This allows users to request catalog generation without needing to install or run the tools locally.

## 🚀 Quick Start

1. **Go to the Issues tab** in the GitHub repository
2. **Click "New Issue"**
3. **Select a catalog type:**
   - 🔄 **Generate Intake v2 Catalog** - Convert Intake v1, Zarr, or Parquet to Intake v2
   - 🗺️ **Generate STAC Catalog** - Create STAC catalogs from Earth System Model data
4. **Fill out the form** with your data source and requirements
5. **Submit the issue**

The forge will automatically:
- ✅ Validate your inputs
- 🔄 Run the catalog generator
- 📦 Create a downloadable artifact
- 💬 Comment on your issue with results and download instructions

## 📋 Issue Templates

### Intake v2 Catalog Generation

**Use case:** Convert existing catalogs or data stores to Intake v2 format

**Required fields:**
- **Source URI** - URL or path to input (e.g., `https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml`)
- **Output Catalog Name** - Name for the generated catalog
- **Source Type** - Type of input (Intake v1, Zarr, Parquet, or Auto-detect)

**Optional fields:**
- Additional command-line options
- Description
- Visibility settings

**Example:**
```
Source URI: https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml
Output Name: hackathon-intake-v2
Source Type: Intake v1 YAML Catalog
Description: Digital Earth's Global Hackathon catalog converted to Intake v2
```

### STAC Catalog Generation

**Use case:** Generate STAC collections from Earth System Model output

**Required fields:**
- **Data Source URI** - URL or path to the dataset
- **Collection ID** - Unique identifier for the collection
- **Project ID** - Project identifier (e.g., EERIE, NextGEMS)
- **Description** - Detailed description of the dataset

**Optional fields:**
- Source ID (model name)
- Experiment ID
- Spatial/temporal extent
- STAC API URL for publishing
- Template and preview options

**Example:**
```
Data Source: https://example.com/data/icon-ngc4008.zarr
Collection ID: eerie-icon-ngc4008
Project ID: EERIE
Source ID: ICON
Experiment ID: ngc4008
Description: ICON high-resolution atmospheric data from the EERIE project
```

## 🏷️ Labels

The forge uses labels to trigger different workflows:

- **`forge-intake`** - Triggers Intake v2 catalog generation
- **`forge-stac`** - Triggers STAC catalog generation
- **`forge-complete`** - Added automatically when generation succeeds
- **`forge-failed`** - Added automatically when generation fails

These labels are automatically applied by the issue templates.

## 📦 Accessing Generated Catalogs

After the forge completes:

1. **Check the issue comments** - A bot will comment with status and instructions
2. **Go to the Actions tab** - Find the workflow run for your issue
3. **Download the artifact** - Named `catalog-issue-<number>`
4. **Extract and use** - The artifact contains your generated catalog

**Artifact retention:** 90 days

## 🔧 Testing Locally

You can test the forge parser locally before creating an issue:

```bash
# Set up environment
export CATALOG_TYPE="intake"
export ISSUE_NUMBER="test"
export ISSUE_BODY="### Source URI
https://example.com/catalog.yaml

### Output Catalog Name
my-catalog"

# Run the parser
python .github/scripts/forge_parser.py
```

The output will be in the `forge_output/` directory.

## 🔄 Workflow Details

### Trigger Conditions

The workflow triggers when:
- A new issue is opened with `forge-intake` or `forge-stac` label
- A label is added to an existing issue

### Pipeline Steps

1. **Parse Issue** - Extract form fields from issue body
2. **Setup Environment** - Install Python and dependencies
3. **Run Generator** - Execute the appropriate catalog generator
4. **Upload Artifact** - Package outputs for download
5. **Comment Result** - Post status and instructions to the issue
6. **Add Status Label** - Mark as complete or failed

### Timeouts

- Individual commands: 10 minutes maximum
- Total workflow: 60 minutes (GitHub default)

## 🎯 Use Cases

### Converting Legacy Catalogs

**Problem:** You have an Intake v1 YAML catalog that needs to be migrated to Intake v2

**Solution:** Use the Intake forge with:
- Source URI pointing to your v1 catalog
- Source Type: "Intake v1 YAML Catalog"

### Cataloging New Datasets

**Problem:** You have Earth System Model output in Zarr format that needs a STAC catalog

**Solution:** Use the STAC forge with:
- Data Source URI pointing to your Zarr store
- Proper metadata (project, experiment, model info)

### Batch Processing

**Problem:** You need to generate multiple catalogs

**Solution:** Create multiple issues (one per catalog). The forge will process them in parallel.

## 🛠️ Advanced Configuration

### Custom Options for Intake

You can pass additional command-line options to `tointake2` using the "Additional Options" field:

```
--verbose
--include-pattern '*.zarr'
--exclude-pattern 'scratch/*'
--allow-missing
```

### STAC Templates

For STAC generation, you can:
- Use EERIE Cloud templates (checkbox option)
- Generate preview thumbnails (checkbox option)
- Include Kerchunk references (checkbox option)

## 📊 Monitoring

### Check Workflow Status

1. Go to **Actions** tab in the repository
2. Filter by workflow: **"Forge Catalog"**
3. Find your issue number in the run title
4. View logs for detailed progress

### Debugging Failed Runs

If the forge fails:
1. **Check the error comment** on your issue
2. **View the full logs** in the Actions tab
3. **Verify your inputs** match the required format
4. **Check data accessibility** - ensure URLs are publicly accessible
5. **Try the test command locally** to reproduce the issue

## 🔐 Security Considerations

- **Public repositories**: Anyone can create issues and trigger workflows
- **Rate limiting**: GitHub has limits on workflow minutes
- **Access control**: Input URIs must be publicly accessible or authenticated via environment
- **Artifact access**: Only users with read access to the repository can download artifacts

## 🚧 Limitations

- **Artifact size**: GitHub has a 10GB limit per artifact
- **Retention**: Artifacts are kept for 90 days
- **Timeout**: Long-running generations may timeout (10 min per command)
- **Dependencies**: Some STAC features require external services (EERIE Cloud, STAC APIs)

## 🔮 Future Enhancements

Planned improvements:
- [ ] Full STAC item generation (currently creates collections only)
- [ ] Direct publishing to STAC APIs
- [ ] Support for private data sources with credentials
- [ ] Email notifications when catalogs are ready
- [ ] Preview/validation before full generation
- [ ] Scheduled catalog updates for dynamic datasets
- [ ] Integration with object storage (S3, Swift)

## 📚 Related Documentation

- [Main README](../README.md) - Installation and basic usage
- [Setup Guide](../SETUP_GUIDE.md) - Development setup
- [tointake2 Documentation](../src/generators/intake/v2/) - Intake generator details
- [STAC Documentation](../src/generators/stac/) - STAC generator details

## 💡 Tips

1. **Start small** - Test with a small dataset first
2. **Use descriptive names** - Make output names meaningful
3. **Add descriptions** - Help others understand your catalog
4. **Check examples** - Look at previous successful issues
5. **Be patient** - Large datasets take time to process

## 🐛 Reporting Issues

If you encounter problems with the forge:
1. Create a regular issue (not a forge template)
2. Label it with `bug` and `forge`
3. Include:
   - Link to the failed forge issue
   - Error messages from the comments
   - Expected vs actual behavior
