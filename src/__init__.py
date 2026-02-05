"""
2catalogs - Code that generates catalogs for Earth System Model output.

This package provides tools for generating intake and STAC catalogs.
The 'intake' and 'stac' modules are optional and can be installed separately.
"""

__version__ = "0.1.0"

__all__ = ["generators"]


def __getattr__(name):
    """Lazy import for optional dependencies."""
    if name == "intake":
        try:
            from . import generators
            return generators
        except ImportError as e:
            raise ImportError(
                f"The 'intake' functionality requires additional dependencies. "
                f"Install them with: pip install 2catalogs[intake]\n"
                f"Original error: {e}"
            ) from e
    elif name == "stac":
        try:
            from . import generators
            return generators
        except ImportError as e:
            raise ImportError(
                f"The 'stac' functionality requires additional dependencies. "
                f"Install them with: pip install 2catalogs[stac]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
