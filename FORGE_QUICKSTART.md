# Forge Quick Start

**TL;DR:** Generate catalogs automatically through GitHub Issues. No installation needed!

## 🚀 3-Step Process

### Step 1: Click "New Issue"

Go to the [Issues tab](../../issues/new/choose) and choose your catalog type:
- 🔄 **Generate Intake v2 Catalog** (for Intake v1 → v2 conversion)
- 🗺️ **Generate STAC Catalog** (for Earth System Model data)

### Step 2: Fill the Form

**For Intake v2:**
```
Source URI: https://your-catalog-url/catalog.yaml
Output Name: my-catalog-v2
Source Type: Intake v1 YAML Catalog
```

**For STAC:**
```
Data Source: https://your-data-url/dataset.zarr
Collection ID: my-collection
Project ID: MY-PROJECT
Description: My awesome dataset
```

### Step 3: Download Results

1. Wait for the bot to comment (~2-5 minutes)
2. Click the Actions link in the comment
3. Download the `catalog-issue-XXX` artifact
4. Extract and use your catalog!

## 💡 Real Example

**Input:** `https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml`

**Output:** An Intake v2 catalog in YAML format, ready to use!

## 🧪 Test Locally First (Optional)

```bash
# Install
pip install -e ".[intake]"

# Test
python test_forge.py intake \
  --uri "https://example.com/catalog.yaml" \
  --name "test"

# Check output
ls forge_output/
```

## 📚 Learn More

- [Full Documentation](FORGE.md) - Detailed usage guide
- [Examples](FORGE_EXAMPLES.md) - Common scenarios
- [Architecture](FORGE_ARCHITECTURE.md) - How it works

## ❓ FAQ

**Q: Do I need to install anything?**
A: No! Just create an issue. The forge runs on GitHub's servers.

**Q: How long do artifacts last?**
A: 90 days

**Q: Can I process private data?**
A: Currently only publicly accessible URLs are supported.

**Q: What if it fails?**
A: The bot will comment with error details. Check the logs and try again.

**Q: Can I batch process?**
A: Yes! Create multiple issues, they'll run in parallel.

## 🎯 Use Cases

- ✅ Convert legacy Intake v1 catalogs to v2
- ✅ Generate STAC collections for model output
- ✅ Catalog Zarr stores
- ✅ Process Kerchunk references
- ✅ Batch catalog generation

## 🛠️ Under the Hood

```
Issue → GitHub Actions → Parser → Generator → Catalog → Artifact
```

Simple, automatic, and reliable!

---

**Ready?** [Create your first issue now!](../../issues/new/choose) 🚀
