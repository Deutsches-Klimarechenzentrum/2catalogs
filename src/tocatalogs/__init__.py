"""Generators package for creating catalogs."""

__all__ = ["intake", "stac"]


def __getattr__(name):
    """Lazy import for optional generator modules."""
    if name == "intake":
        try:
            from . import intake as _intake
            return _intake
        except ImportError as e:
            raise ImportError(
                f"The 'intake' generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[intake]\n"
                f"Original error: {e}"
            ) from e
    elif name == "stac":
        try:
            from . import stac as _stac
            return _stac
        except ImportError as e:
            raise ImportError(
                f"The 'stac' generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[stac]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
