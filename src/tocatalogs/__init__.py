"""Generators package for creating catalogs."""

__all__ = ["intake", "stac"]


def __getattr__(name):
    """Lazy import for optional generator modules."""
    if name == "intake":
        try:
            import importlib
            return importlib.import_module('.intake', __name__)
        except ImportError as e:
            raise ImportError(
                f"The 'intake' generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[intake]\n"
                f"Original error: {e}"
            ) from e
    elif name == "stac":
        try:
            import importlib
            return importlib.import_module('.stac', __name__)
        except ImportError as e:
            raise ImportError(
                f"The 'stac' generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[stac]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
