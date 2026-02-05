"""STAC catalog generators."""

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
            if name == "create_collection":
                from . import create_collection as module
            elif name == "create_with_eeriecloud":
                from . import create_with_eeriecloud as module
            elif name == "xarray_dataset_to_stac_item":
                from . import xarray_dataset_to_stac_item as module
            elif name == "utils":
                from . import utils as module
            return module
        except ImportError as e:
            raise ImportError(
                f"The STAC generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[stac]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
