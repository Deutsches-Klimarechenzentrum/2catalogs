# Forge Setup Checklist

Quick verification checklist for the forge mechanism configuration.

## ✅ Required Files

- [ ] `.github/workflows/forge-catalog.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/forge-intake.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/forge-stac.yml` exists
- [ ] `.github/scripts/forge_parser.py` exists
- [ ] `.gitlab/scripts/forge_parser.py` exists (for GitLab integration)

## 🏷️ GitHub Labels

Create these labels (Settings → Labels):

- [ ] `forge-intake` - Request Intake v2 catalog generation (color: `0E8A16`)
- [ ] `forge-stac` - Request STAC catalog generation (color: `1D76DB`)
- [ ] `forge-complete` - Generation completed (color: `0E8A16`)
- [ ] `forge-failed` - Generation failed (color: `D73A4A`)

## 🧪 Quick Test

```bash
# Test locally with test script
python tests/test_forge.py intake \
  --uri "https://example.com/catalog.yaml" \
  --name "test" \
  --description "Test catalog"
```

## 🚀 Verification

1. **Issue Templates**: Visit `github.com/<owner>/<repo>/issues/new/choose`
   - [ ] Templates appear correctly
   - [ ] Fields validate properly

2. **Workflows**: Check Actions tab
   - [ ] Workflows are enabled
   - [ ] No syntax errors

3. **Real Test**: Create a test issue
   - [ ] Workflow triggers automatically
   - [ ] Catalog generates successfully
   - [ ] Artifact downloads correctly
   - [ ] Issue comment appears

## 📋 GitLab Integration

For GitLab CI/CD forge jobs:

- [ ] `.gitlab-ci.yml` includes forge jobs
- [ ] `ISSUE_BODY` variable can be set manually
- [ ] Artifacts are configured correctly
- [ ] Pages deployment works

## ✨ Success Criteria

The forge is ready when:

1. ✅ All required files exist
2. ✅ Labels are created
3. ✅ Issue templates work
4. ✅ Test issue completes successfully
5. ✅ Documentation is accessible

---

For detailed setup instructions, see [FORGE.md](FORGE.md).  
For architecture details, see [FORGE_ARCHITECTURE.md](FORGE_ARCHITECTURE.md).
