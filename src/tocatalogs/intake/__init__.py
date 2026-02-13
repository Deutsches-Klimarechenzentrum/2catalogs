"""Intake catalog generators."""

__all__ = ["v2"]

# Lazy loading for intake-specific modules
def __getattr__(name):
    """Lazy import for intake modules."""
    if name == "v2":
        try:
            import importlib
            return importlib.import_module('.v2', __name__)
        except ImportError as e:
            raise ImportError(
                f"The intake generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[intake]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
