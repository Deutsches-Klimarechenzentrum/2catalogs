# GitHub Labels for 2catalogs Repository

This file documents the labels used in the repository, particularly for the forge mechanism.

## Forge Labels

These labels are used by the automated catalog generation pipeline:

### Trigger Labels
- **`forge-intake`** 🔄
  - Color: `#0E8A16` (green)
  - Description: Request Intake v2 catalog generation
  - Automatically applied by the Intake issue template

- **`forge-stac`** 🗺️
  - Color: `#1D76DB` (blue)
  - Description: Request STAC catalog generation
  - Automatically applied by the STAC issue template

- **`forge-all`** 🚀
  - Color: `#6F42C1` (purple)
  - Description: Request generation of all catalog types
  - Note: This label is not used directly; the "Generate All Catalogs" template applies both `forge-intake` and `forge-stac` labels

### Status Labels
- **`forge-complete`** ✅
  - Color: `#0E8A16` (green)
  - Description: Catalog generation completed successfully
  - Automatically applied by workflow

- **`forge-failed`** ❌
  - Color: `#D73A4A` (red)
  - Description: Catalog generation failed
  - Automatically applied by workflow

## Creating Labels

You can create these labels manually via the GitHub UI, or use the GitHub CLI:

```bash
# Create forge labels
gh label create "forge-intake" --color "0E8A16" --description "Request Intake v2 catalog generation"
gh label create "forge-stac" --color "1D76DB" --description "Request STAC catalog generation"
gh label create "forge-complete" --color "0E8A16" --description "Catalog generation completed"
gh label create "forge-failed" --color "D73A4A" --description "Catalog generation failed"

# Create standard labels
gh label create "bug" --color "D73A4A" --description "Something isn't working"
gh label create "enhancement" --color "A2EEEF" --description "New feature or request"
gh label create "documentation" --color "0075CA" --description "Improvements or additions to documentation"
gh label create "question" --color "D876E3" --description "Further information is requested"
```

## Label Workflow

1. User creates issue using template → `forge-intake` or `forge-stac` label applied
2. Workflow triggers on label
3. Catalog generation runs
4. On success → `forge-complete` label added
5. On failure → `forge-failed` label added

## Filtering Issues

You can filter issues by forge labels:

- All forge requests: `label:forge-intake,forge-stac`
- Completed forges: `label:forge-complete`
- Failed forges: `label:forge-failed`
- Pending forges: `label:forge-intake,forge-stac -label:forge-complete -label:forge-failed`
