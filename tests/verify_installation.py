#!/usr/bin/env python3
"""
Quick verification script to test 2catalogs installation.

This script tests that the package is installed correctly and that
optional dependencies work as expected.
"""

def test_core_import():
    """Test core package import."""
    try:
        import generators
        print("✓ Core package imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Core package import failed: {e}")
        return False


def test_intake_import():
    """Test intake module import."""
    try:
        from generators.intake.v2 import tointake2
        print("✓ Intake module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Intake module import failed (install with: pip install 2catalogs[intake])")
        print(f"  Error: {e}")
        return False


def test_stac_import():
    """Test STAC module import."""
    try:
        from generators.stac import create_collection
        print("✓ STAC module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ STAC module import failed (install with: pip install 2catalogs[stac])")
        print(f"  Error: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing 2catalogs installation...\n")
    
    results = {
        "core": test_core_import(),
        "intake": test_intake_import(),
        "stac": test_stac_import(),
    }
    
    print("\n" + "="*50)
    print("Summary:")
    print("="*50)
    
    if results["core"]:
        print("Core package: OK")
    else:
        print("Core package: FAILED")
    
    if results["intake"]:
        print("Intake support: OK")
    else:
        print("Intake support: Not installed (optional)")
    
    if results["stac"]:
        print("STAC support: OK")
    else:
        print("STAC support: Not installed (optional)")
    
    print("\nTo install optional dependencies:")
    if not results["intake"]:
        print("  pip install 2catalogs[intake]")
    if not results["stac"]:
        print("  pip install 2catalogs[stac]")
    print("  pip install 2catalogs[all]  # Install all optional dependencies")


if __name__ == "__main__":
    main()
