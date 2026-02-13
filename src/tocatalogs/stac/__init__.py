"""STAC catalog generators."""

import sys

__all__ = [
    "create_collection",
    "create_with_eeriecloud",
    "xarray_dataset_to_stac_item",
    "utils",
]

def __getattr__(name):
    """Lazy import for STAC modules."""
    if name in __all__:
        try:
            # Import the module and return it from sys.modules to avoid recursion
            if name == "create_collection":
                import tocatalogs.stac.create_collection
                return sys.modules['tocatalogs.stac.create_collection']
            elif name == "create_with_eeriecloud":
                import tocatalogs.stac.create_with_eeriecloud
                return sys.modules['tocatalogs.stac.create_with_eeriecloud']
            elif name == "xarray_dataset_to_stac_item":
                import tocatalogs.stac.xarray_dataset_to_stac_item
                return sys.modules['tocatalogs.stac.xarray_dataset_to_stac_item']
            elif name == "utils":
                import tocatalogs.stac.utils
                return sys.modules['tocatalogs.stac.utils']
        except ImportError as e:
            raise ImportError(
                f"The STAC generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[stac]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
