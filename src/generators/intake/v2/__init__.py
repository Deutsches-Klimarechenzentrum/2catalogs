"""Intake v2 catalog generator."""

__all__ = ["tointake2"]

def __getattr__(name):
    """Lazy import for intake v2 modules."""
    if name == "tointake2":
        try:
            from . import tointake2 as module
            return module
        except ImportError as e:
            raise ImportError(
                f"The intake v2 generator requires additional dependencies. "
                f"Install them with: pip install 2catalogs[intake]\n"
                f"Original error: {e}"
            ) from e
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
