# Development Setup Guide

## Quick Start

1. **Clone the repository** (if not already done)
   ```bash
   cd /path/to/2catalogs
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install the package in development mode**
   
   Choose one of the following based on your needs:
   
   ```bash
   # Minimal installation (core only)
   pip install -e .
   
   # With development tools and all features
   pip install -e ".[dev,all]"
   
   # Or specific features
   pip install -e ".[dev,intake]"  # Intake + dev tools
   pip install -e ".[dev,stac]"    # STAC + dev tools
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Verify installation**
   ```bash
   python tests/verify_installation.py
   ```

## Pre-commit Hooks

After installing pre-commit hooks, they will run automatically on every commit. The hooks will:

- Format your code with Black
- Sort imports with isort
- Lint code with Ruff
- Check types with mypy
- Validate file formats (YAML, JSON, etc.)
- Check docstrings

### Running hooks manually

```bash
# Run on staged files only
pre-commit run

# Run on all files
pre-commit run --all-files

# Run a specific hook
pre-commit run black --all-files
pre-commit run ruff --all-files
```

### Skipping hooks (use sparingly!)

If you need to skip pre-commit hooks for a specific commit:
```bash
git commit --no-verify -m "Your commit message"
```

## Code Quality Standards

This project follows these standards:

- **Line length**: 100 characters
- **Code formatter**: Black
- **Import sorting**: isort (Black-compatible profile)
- **Linter**: Ruff
- **Type hints**: Checked with mypy
- **Docstring style**: NumPy convention

## Testing Your Changes

Before submitting changes:

1. Run pre-commit hooks on all files:
   ```bash
   pre-commit run --all-files
   ```

2. Verify imports work correctly:
   ```bash
   python tests/verify_installation.py
   ```

3. Test with both optional dependencies installed and uninstalled to ensure lazy imports work

## Common Issues

### Pre-commit hooks fail to install
```bash
pip install --upgrade pre-commit
pre-commit install
```

### Import errors with optional dependencies
Make sure you've installed the required extras:
```bash
pip install -e ".[all]"
```

### mypy errors
Some dependencies may not have type stubs. This is expected and won't block commits, but you can silence them with:
```python
import something  # type: ignore
```

## Updating Dependencies

To update pre-commit hooks to their latest versions:
```bash
pre-commit autoupdate
```

To update Python dependencies, edit `pyproject.toml` and reinstall:
```bash
pip install -e ".[dev,all]"
```
