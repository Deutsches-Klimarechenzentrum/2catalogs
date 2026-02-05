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
from generators.intake.v2 import tointake2

# Only works if installed with [stac]
from generators.stac import create_collection
```

If you try to use a module without its dependencies installed, you'll get a helpful error message:

```
ImportError: The 'stac' generator requires additional dependencies.
Install them with: pip install 2catalogs[stac]
```

## Project Structure

```
2catalogs/
├── src/
│   ├── generators/
│   │   ├── intake/       # Intake catalog generators
│   │   │   └── v2/
│   │   │       └── tointake2.py
│   │   └── stac/         # STAC catalog generators
│   │       ├── create_collection.py
│   │       ├── create_with_eeriecloud.py
│   │       ├── xarray_dataset_to_stac_item.py
│   │       └── utils/
│   └── display/
├── pyproject.toml        # Package configuration
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
└── README.md
