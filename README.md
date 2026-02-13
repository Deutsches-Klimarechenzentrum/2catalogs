# 2catalogs

This repo contains code that generates catalogs for Earth System Model output.

## Installation

### Basic Installation

Install the core package without optional dependencies:

```bash
pip install -e .
```

### Optional Dependencies

Install with specific catalog generators:

**Intake catalog support:**
```bash
pip install -e ".[intake]"
```

**STAC catalog support:**
```bash
pip install -e ".[stac]"
```

**All catalog generators:**
```bash
pip install -e ".[all]"
```

**Development tools (includes linters, formatters, and pre-commit hooks):**
```bash
pip install -e ".[dev]"
```

### Development Setup

For development, install with all dependencies and set up pre-commit hooks:

```bash
# Install package with dev dependencies
pip install -e ".[dev,all]"

# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files (optional, to test setup)
pre-commit run --all-files
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks run automatically on each commit and include:

- **File checks**: Trailing whitespace, EOF, YAML/JSON validation
- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **Ruff**: Fast Python linting with auto-fixes
- **mypy**: Type checking
- **pydocstyle**: Docstring style checking (NumPy convention)

### Manual Hook Execution

Run hooks on staged files:
```bash
pre-commit run
```

Run hooks on all files:
```bash
pre-commit run --all-files
```

Update hooks to latest versions:
```bash
pre-commit autoupdate
```

## Usage

### Lazy Imports

The package uses lazy imports for optional dependencies. This means you can install only what you need:

```python
# Only works if installed with [intake]
from tocatalogs.intake import v2

# Only works if installed with [stac]
from tocatalogs.stac import create_collection
```

If you try to use a module without its dependencies installed, you'll get a helpful error message:

```
ImportError: The 'stac' generator requires additional dependencies.
Install them with: pip install 2catalogs[stac]
```

## 🚀 Catalog Forge (Automated Generation)

Don't want to install anything? Use the **Catalog Forge** to generate catalogs automatically through GitHub Issues!

### ⚡ Quick Start

1. Go to the [Issues tab](../../issues/new/choose)
2. Select your catalog type (Intake v2 or STAC)
3. Enter your data source URL (e.g., `https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml`)
4. Submit and wait ~2-5 minutes
5. Download your generated catalog!

**📖 [Quick Start Guide](docs/FORGE_QUICKSTART.md)** | **📚 [Full Documentation](docs/FORGE.md)** | **💡 [Examples](docs/FORGE_EXAMPLES.md)**

### Features

- ✅ No local installation required
- 🔄 Automatic catalog generation from GitHub issues
- 📦 Downloadable artifacts (kept for 90 days)
- 💬 Status updates via issue comments
- 🏷️ Support for Intake v2 and STAC catalogs
- 🧪 Local testing tools included

## Project Structure

```
2catalogs/
├── src/
│   ├── tocatalogs/
│   │   ├── intake/       # Intake catalog generators
│   │   │   └── v2/
│   │   │       └── v2.py
│   │   └── stac/         # STAC catalog generators
│   │       ├── create_collection.py
│   │       ├── create_with_eeriecloud.py
│   │       ├── xarray_dataset_to_stac_item.py
│   │       └── utils/
│   └── display/
├── .github/
│   ├── workflows/        # CI/CD pipelines
│   │   └── forge-catalog.yml
│   ├── scripts/          # Automation scripts
│   │   └── forge_parser.py
│   └── ISSUE_TEMPLATE/   # Issue templates for forge
├── pyproject.toml        # Package configuration
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── FORGE.md              # Forge documentation
└── README.md
