# Merge Request Workflow

## Overview

When a catalog is generated via the Forge workflow, instead of automatically committing to the main branch, the system now creates a merge request (MR) in GitLab for review.

## Workflow Steps

1. **User creates GitHub Issue** with forge template
2. **GitHub Action triggers GitLab CI** pipeline
3. **GitLab CI generates catalog** using forge tools
4. **New branch is created** (e.g., `forge/catalog-intake-issue-123`)
5. **Changes committed** to the new branch
6. **Merge Request created** in GitLab
7. **GitHub Issue updated** with MR link
8. **Maintainer reviews** MR in GitLab
9. **Maintainer merges** when satisfied
10. **Catalog added** to main catalog

## Benefits

### Quality Control
- All catalog additions are reviewed before merging
- Prevents accidental or malformed catalog entries
- Allows discussion and iteration on catalog metadata

### Audit Trail
- Clear history of who approved each catalog addition
- MR descriptions include issue context
- Easy to track changes over time

### Collaboration
- Team members can review and comment on MRs
- Multiple reviewers can be assigned
- CI checks can run on MR before merge

## For Maintainers

### Reviewing Merge Requests

1. **Navigate to MR** (link posted in GitHub issue)
2. **Check the changes**:
   - Verify catalog YAML is valid
   - Check metadata completeness
   - Ensure no conflicts with existing entries
3. **Test if needed** (MR pipeline runs automatically)
4. **Approve and merge** when satisfied
5. **GitHub issue automatically closed** (if desired)

### MR Review Checklist

The MR description includes a checklist:

- [ ] Catalog YAML is valid
- [ ] Metadata is complete and accurate
- [ ] No conflicts with existing entries

### Manual Cleanup

If a MR is rejected or needs major changes:

1. Comment on the MR with feedback
2. Close the MR
3. Comment on the GitHub issue explaining what needs to change
4. User can create a new issue with corrections

## Technical Details

### Branch Naming

Branches are automatically named:
```
forge/catalog-{type}-issue-{number}
```

Example: `forge/catalog-intake-issue-42`

### MR Configuration

- **Source branch**: Auto-generated forge branch
- **Target branch**: `main`
- **Auto-remove source branch**: Yes (after merge)
- **Squash commits**: Yes (single commit in main)
- **Labels**: `forge`, `automated`

### Required Permissions

The GitLab CI pipeline requires:

- **CI_PUSH_TOKEN**: GitLab access token with:
  - `api` scope (for creating MRs)
  - `write_repository` scope (for pushing branches)

- **GITHUB_TOKEN**: GitHub token (auto-provided by Actions) for:
  - Posting comments to issues
  - Reading issue content

## Example Flow

### 1. GitHub Issue Created

```
Issue #42: Add new dataset catalog

[forge-intake template filled out]
```

### 2. GitLab CI Runs

```bash
✓ Catalog generated
✓ Branch created: forge/catalog-intake-issue-42
✓ Changes committed
✓ Merge request created: !15
```

### 3. GitHub Issue Updated

```
✅ Catalog generated successfully!

Merge Request: !15 - View on GitLab
https://gitlab.com/project/2catalogs/-/merge_requests/15

Catalog Type: intake

Next Steps
1. Review the merge request on GitLab
2. Check the generated catalog entry
3. Merge when ready
```

### 4. Maintainer Reviews

In GitLab:
- Views diff of `catalog/main.yaml`
- Checks metadata
- Approves and merges

### 5. Catalog Added

After merge:
- Catalog entry in main branch
- Source branch auto-deleted
- MR marked as merged

## Customization

### Auto-merge for Trusted Users

You could extend the script to auto-merge MRs from trusted contributors:

```python
# In create_merge_request.py
if is_trusted_user(issue_author):
    auto_merge_mr(mr_data)
```

### Additional Checks

Add CI jobs that run on MRs:

```yaml
# In .gitlab-ci.yml
validate-catalog:
  stage: test
  script:
    - uv run python scripts/validate_catalog.py
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

### Custom Notifications

Extend the notification to include more details:

```python
# In create_merge_request.py
def notify_github_issue(...):
    # Add catalog preview
    # Add validation results
    # Add estimated review time
```

## Troubleshooting

### MR Not Created

**Symptoms**: Pipeline succeeds but no MR appears

**Solutions**:
- Check CI_PUSH_TOKEN has correct scopes
- Verify token hasn't expired
- Check GitLab API logs in pipeline output

### GitHub Issue Not Updated

**Symptoms**: MR created but issue not notified

**Solutions**:
- Verify GITHUB_TOKEN is passed in pipeline trigger
- Check token has `issues: write` permission
- Review pipeline logs for API errors

### Branch Already Exists

**Symptoms**: Pipeline fails with "branch exists" error

**Solutions**:
- Delete old forge branches manually
- Or modify script to use unique branch names with timestamps:
  ```python
  branch_name = f"forge/catalog-{catalog_type}-issue-{issue_number}-{timestamp}"
  ```
