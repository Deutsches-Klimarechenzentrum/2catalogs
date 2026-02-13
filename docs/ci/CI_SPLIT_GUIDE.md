# GitLab and GitHub

## Overview

The CI/CD workload has been split between GitLab CI and GitHub Actions to optimize resources and leverage each platform's strengths.

---

## 🔷 GitLab CI/CD - Catalog Generation (Forge)

**Location**: `.gitlab-ci.yml`

**Primary Responsibilities**:
- ✅ Catalog generation (Forge system)
- ✅ Manual forge jobs (Intake, STAC, All)
- ✅ Auto-commit forge results
- ✅ GitLab Pages deployment
- ✅ Issue-based automation (future)

**Key Features**:
- Uses **conda runner** exclusively (all jobs tagged with `tags: [conda]`)
- Single Python environment (3.11 via conda)
- Focused on catalog generation workflow
- Reduced complexity and faster execution

**Pipeline Stages**:
1. **forge** - Catalog generation jobs
2. **deploy** - GitLab Pages deployment

**Trigger Conditions**:
- Commits to `main` branch (for Pages)
- Manual pipeline runs (for forge jobs)
- Webhook triggers (for issue automation)

---

## 🔶 GitHub Actions - Testing and Quality

**Location**: `.github/workflows/ci.yml`

**Primary Responsibilities**:
- ✅ Multi-version Python testing (3.9, 3.10, 3.11, 3.12)
- ✅ Code linting and quality checks
- ✅ Package building and validation
- ✅ Import verification
- ✅ Basic integration tests

**Key Features**:
- Matrix testing across multiple Python versions
- Extensive test coverage
- Code quality enforcement
- PR/MR validation

**Jobs**:
1. **test** - Test on Python 3.9-3.12
2. **lint** - Code quality checks (ruff)
3. **build** - Package building (on main branch)

**Trigger Conditions**:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Manual workflow dispatch

---

## 🚫 Disabled Workflows

### GitHub Forge Workflow (DISABLED)

**Location**: `.github/workflows/forge-catalog.yml`

**Status**: ⛔ **DISABLED**

**Reason**: Forge functionality moved to GitLab CI/CD

The issue-triggered forge automation is now handled exclusively by GitLab. This workflow has been disabled with:
- Issue trigger commented out
- `if: false` condition to skip execution
- Notice job explaining the move

---

## 📊 Responsibility Matrix

| Task | GitHub Actions | GitLab CI/CD |
|------|----------------|--------------|
| **Testing** |
| Multi-version Python tests | ✅ | ❌ |
| Import verification | ✅ | ❌ |
| Integration tests | ✅ | ❌ |
| **Quality** |
| Linting (ruff) | ✅ | ❌ |
| Code quality checks | ✅ | ❌ |
| **Building** |
| Package building | ✅ | ❌ |
| Package validation | ✅ | ❌ |
| **Forge** |
| Catalog generation | ❌ | ✅ |
| Manual forge jobs | ❌ | ✅ |
| Auto-commit results | ❌ | ✅ |
| Issue automation | ❌ | ✅ |
| **Deployment** |
| GitLab Pages | ❌ | ✅ |

---

## 🔧 Configuration Requirements

### GitLab CI/CD Setup

**Required Placeholders** in `.gitlab-ci.yml`:
```yaml
<CONDA_ENV_NAME>              → catalog-forge (or your choice)
<PAGES_BRANCH>                → main
<DEPLOY_URL>                  → https://yourproject.gitlab.io
<API_BASE_URL>                → https://api.example.com (optional)
<ARTIFACT_RETENTION_DAYS>     → 90
```

**Required CI/CD Variables** (Settings > CI/CD > Variables):
- `CI_PUSH_TOKEN`: Personal access token with `write_repository` scope

**Required Runner**:
- Conda runner with tag: `conda`
- Must have conda installed and configured
- Python 3.11 environment

### GitHub Actions Setup

**No additional configuration needed** - works out of the box!

**Optional**:
- Configure branch protection rules
- Set up required status checks

---

## 🏃 Using the Split CI/CD

### For Testing and Quality (GitHub)

```bash
# Push to trigger tests
git push origin main

# Create PR to trigger tests
gh pr create --base main --head feature-branch
```

**Automatic triggers**:
- Every push to `main` or `develop`
- Every pull request
- Manual workflow dispatch

### For Catalog Generation (GitLab)

**Manual forge job**:
1. Go to GitLab: **CI/CD > Pipelines**
2. Click **Run Pipeline**
3. Select branch: `main`
4. Add variables:
   ```
   CATALOG_TYPE: intake
   ISSUE_BODY: <paste forge template>
   ISSUE_NUMBER: manual-001
   ```
5. Click **Run Pipeline**
6. Find and click ▶️ on the forge job
7. Download artifacts after completion

**Via GitLab Issues** (recommended):
1. Create issue using forge template
2. Fill in catalog details
3. Add label: `forge-intake` or `forge-stac`
4. **(Future)** Webhook triggers pipeline automatically

---

## 🎯 Benefits of the Split

### GitHub Actions Strengths
✅ **Matrix testing** - Easy multi-version Python testing  
✅ **Fast runners** - Quick execution for tests  
✅ **PR integration** - Excellent PR/MR validation  
✅ **Marketplace** - Rich ecosystem of actions  
✅ **Generous limits** - 2000+ free minutes/month  

### GitLab CI/CD Strengths
✅ **Custom runners** - Use your conda-equipped runners  
✅ **Environment control** - Precise conda environment management  
✅ **Manual jobs** - Easy manual trigger workflow  
✅ **Artifact management** - Powerful artifact handling  
✅ **Pages integration** - Native GitLab Pages support  

### Overall Benefits
- ⚡ **Faster pipelines** - Each platform does what it's best at
- 💰 **Cost efficient** - Reduced minutes usage on both platforms
- 🎨 **Clean separation** - Clear responsibility boundaries
- 🔧 **Better fit** - Tools matched to tasks
- 📦 **Resource optimization** - Conda runner only where needed

---

## 🗺️ Workflow Diagrams

### GitHub Actions Flow
```
Push/PR → Test (3.9-3.12) → Lint → Build → ✅
          ↓
          - Import checks
          - Unit tests
          - Coverage reports
```

### GitLab CI/CD Flow
```
Manual/Webhook → Forge Job → Results → Auto-commit (optional)
                 ↓
                 - Parse input
                 - Generate catalog
                 - Save artifacts
                 
Main branch → Pages Deploy → 🌐 GitLab Pages
```

---

## 📝 Migration Notes

### What Changed

**Before**:
- All work in one platform (likely GitHub)
- Heavy forge testing in CI
- Duplicate testing across platforms

**After**:
- Split responsibilities
- Forge only on GitLab with conda
- Testing only on GitHub with multiple Python versions
- No duplicate work

### Breaking Changes

❌ **GitHub issue-triggered forge** - No longer works  
✅ **Use GitLab issues instead**

❌ **GitHub forge workflow** - Disabled  
✅ **Use GitLab manual pipelines**

### Non-Breaking

✅ **GitHub testing** - Still works as before  
✅ **GitHub PR checks** - Still works  
✅ **Package building** - Still works  

---

## 🔍 Troubleshooting

### GitLab CI Issues

**Pipeline doesn't start**:
- Check workflow rules in `.gitlab-ci.yml`
- Ensure runner is available with `conda` tag
- Verify CI/CD is enabled in settings

**Conda environment fails**:
- Check runner has conda installed
- Verify `CONDA_ENV_NAME` variable is set
- Check conda base path is correct

**Forge job fails**:
- Verify `ISSUE_BODY` format matches templates
- Check all required dependencies are installed
- Review `forge_output/error.log` in artifacts

### GitHub Actions Issues

**Tests fail on specific Python version**:
- Check dependency compatibility
- Review test logs for that version
- May need version-specific fixes

**Lint/ruff not working**:
- Install ruff: `pip install ruff`
- Check src/ directory exists
- Verify code follows formatting rules

---

## 📚 Additional Documentation

- **GitLab CI Configuration**: [.gitlab/GITLAB_CONFIGURATION.md](.gitlab/GITLAB_CONFIGURATION.md)
- **GitLab Migration Guide**: [.gitlab/MIGRATION_GUIDE.md](.gitlab/MIGRATION_GUIDE.md)
- **GitLab Quick Reference**: [.gitlab/QUICK_REFERENCE.md](.gitlab/QUICK_REFERENCE.md)
- **GitHub Actions**: [.github/workflows/](.github/workflows/)

---

## 🎓 Best Practices

### Do's
✅ Use GitHub for all testing and quality checks  
✅ Use GitLab for all forge operations  
✅ Configure conda runner properly for GitLab  
✅ Keep forge templates updated in both repos  
✅ Monitor both CI/CD dashboards  

### Don'ts
❌ Don't run forge on GitHub (waste of resources)  
❌ Don't duplicate tests across platforms  
❌ Don't mix responsibilities between platforms  
❌ Don't forget to sync code between GitHub and GitLab  
❌ Don't skip setting up the conda runner  

---

## 🚀 Quick Start Checklist

### GitLab Setup
- [ ] Replace placeholders in `.gitlab-ci.yml`
- [ ] Set up `CI_PUSH_TOKEN` variable
- [ ] Configure conda runner with `conda` tag
- [ ] Test manual forge job
- [ ] Configure GitLab Pages (optional)

### GitHub Setup
- [ ] Verify GitHub Actions are enabled
- [ ] Check test workflow runs on PR
- [ ] Review status checks configuration
- [ ] (Optional) Set up branch protection

### Both Platforms
- [ ] Sync repository between GitHub and GitLab
- [ ] Update team on new workflow
- [ ] Document custom procedures
- [ ] Test end-to-end workflow

---

## 💡 Tips

1. **Sync regularly**: Keep both repos in sync
   ```bash
   git push github main
   git push gitlab main
   ```

2. **Use the right platform**: 
   - Testing? → GitHub
   - Forge? → GitLab

3. **Monitor both**: Check both CI/CD dashboards

4. **Maintain templates**: Keep forge templates identical in both repos

5. **Leverage strengths**: Use each platform for what it does best

---

## 🆘 Getting Help

**GitLab Issues**: Create issue on GitLab repo  
**GitHub Issues**: Create issue on GitHub repo  
**General Questions**: Check documentation first  
**Urgent Issues**: Contact maintainers directly  

---

**Last Updated**: February 6, 2026  
**Version**: 1.0.0  
**Status**: ✅ Active
