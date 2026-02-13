# Community Catalog

The 2catalogs project hosts a **community catalog** that aggregates all publicly shared Intake v2 catalogs generated through the forge.

## 📍 Access the Catalog

Visit the live catalog at: **https://yourusername.github.io/2catalogs**

## ✨ Features

### Interactive Web Interface
- **Browse** all public catalogs with search functionality
- **View statistics** including total catalogs and last update date
- **Select multiple** catalogs to create a custom catalog
- **Download** a merged catalog file with your selection (client-side, no server needed)

### Automatic Integration
When you create a catalog via the forge and mark it as **"Make this catalog publicly accessible"**, it will:
1. ✅ Be automatically added to the community catalog
2. 🔍 Be checked for duplicates (warns if name already exists)
3. 🌐 Become browsable on the web interface immediately after merge
4. 📦 Be available for others to include in their selections

## 🚀 Contributing Your Catalog

1. **Create an issue** using one of the forge templates:
   - 🔄 Generate Intake v2 Catalog
   - 🚀 Generate All Catalogs

2. **Check "Make this catalog publicly accessible"** in the form

3. **Choose a unique name** for your catalog (the pipeline will warn if it's a duplicate)

4. **Wait for generation** - Your catalog will be:
   - Generated and available as an artifact
   - Added to the main community catalog (if not duplicate)
   - Committed to the repository automatically

## 🔍 Duplicate Detection

The forge automatically checks if a catalog with the same name already exists:

- ✅ **Unique name**: Catalog is added to the main catalog
- ⚠️ **Duplicate name**: You'll receive a warning in the issue thread
  - Your catalog is still generated and available as an artifact
  - It's NOT added to the main catalog to avoid conflicts
  - You can create a new issue with a different name

## 📥 Using the Community Catalog

### From the Web Interface
1. Visit the catalog website
2. Browse and search for catalogs
3. Select the ones you want
4. Click "Download Selected" to get a custom YAML file

### Direct Access
Download the complete catalog:
```bash
wget https://yourusername.github.io/2catalogs/catalog/main.yaml
```

### In Your Code
```python
import intake

# Load the entire community catalog
catalog = intake.open_catalog('https://yourusername.github.io/2catalogs/catalog/main.yaml')

# List all available sources
print(catalog.list())

# Access a specific source
data = catalog.your_catalog_name.read()
```

## 📊 Catalog Structure

The main catalog (`catalog/main.yaml`) follows the Intake v2 format:

```yaml
metadata:
  version: 1
  name: "2catalogs Community Catalog"
  description: "Publicly contributed Intake v2 catalogs"
  last_updated: "2026-02-05"

sources:
  example-catalog:
    driver: "intake.catalog.local.YAMLFileCatalog"
    description: "Example catalog description"
    args:
      path: "{{ CATALOG_DIR }}/generated/example-catalog.yaml"
    metadata:
      source_uri: "https://example.com/data.zarr"
      added: "2026-02-05"
      issue: "42"
      project: "EERIE"
```

## 🛠️ Technical Details

### How It Works
1. **Issue Creation**: User creates issue with forge template
2. **Catalog Generation**: GitHub Action runs the forge pipeline
3. **Duplicate Check**: Parser checks if catalog name exists
4. **Catalog Merge**: If unique and public, adds entry to `catalog/main.yaml`
5. **Commit & Push**: Bot commits the updated catalog
6. **GitHub Pages**: Automatically deploys the updated website

### Client-Side Download
The web interface uses JavaScript to:
- Load the YAML catalog (via js-yaml)
- Filter and select catalogs client-side
- Generate custom YAML files on-the-fly
- Trigger browser downloads without server processing

All processing happens in your browser - no server-side code needed!

## 🔒 Privacy

- Only catalogs marked as **"publicly accessible"** are added
- Private catalogs are still generated but remain as artifacts
- All public catalogs are visible on the web interface
- Catalog metadata includes the source GitHub issue number

## 💡 Best Practices

- ✅ Use **descriptive, unique names** for your catalogs
- ✅ Provide **clear descriptions** so others can find your data
- ✅ Include **project information** for better organization
- ✅ Check the web interface to avoid duplicate names
- ❌ Don't use generic names like "catalog" or "data"

## 🙋 Questions?

- Check existing catalogs on the [web interface](https://yourusername.github.io/2catalogs)
- Review [forge documentation](forge/FORGE.md)
- Open a discussion or issue on GitHub
