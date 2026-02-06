#!/bin/bash
# ============================================================================
# UV Setup Script for Local Development
# ============================================================================
# This script installs UV and generates the uv.lock file needed for GitLab CI

set -e

echo "=== UV Setup for 2catalogs ==="

# Check if uv is already installed
if command -v uv &> /dev/null; then
    echo "✓ UV is already installed: $(uv --version)"
else
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✓ UV installed: $(uv --version)"
fi

# Navigate to project root
cd "$(dirname "$0")/../.."

# Generate uv.lock file
echo ""
echo "Generating uv.lock file..."
if [ -f "uv.lock" ]; then
    echo "⚠️  uv.lock already exists, will update it"
fi

uv lock

echo ""
echo "✓ uv.lock generated successfully"

# Optionally sync dependencies
read -p "Do you want to sync dependencies now? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Syncing dependencies..."
    uv sync --all-extras
    echo "✓ Dependencies synced"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Commit the uv.lock file: git add uv.lock && git commit -m 'Add uv.lock for GitLab CI'"
echo "2. Push to GitLab to trigger the pipeline"
echo ""
echo "To run commands with UV:"
echo "  uv run python your_script.py"
echo "  uv run pytest"
echo ""
echo "To add dependencies:"
echo "  uv add package-name"
echo "  uv lock  # Update lock file"
