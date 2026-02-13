# Forge Setup Checklist

Use this checklist to verify that the forge mechanism is properly configured in your repository.

## ✅ Repository Setup

### Files in Place

- [ ] `.github/workflows/forge-catalog.yml` exists
- [ ] `.github/workflows/test-forge.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/forge-intake.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/forge-stac.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/config.yml` exists
- [ ] `.github/scripts/forge_parser.py` exists (and is executable)
- [ ] `tests/test_forge.py` exists (and is executable)

### Documentation

- [ ] `FORGE.md` exists
- [ ] `FORGE_QUICKSTART.md` exists
- [ ] `FORGE_EXAMPLES.md` exists
- [ ] `FORGE_ARCHITECTURE.md` exists
- [ ] `.github/LABELS.md` exists
- [ ] `README.md` includes forge section

### Package Configuration

- [ ] `pyproject.toml` has `[intake]` extras
- [ ] `pyproject.toml` has `[stac]` extras
- [ ] Generator modules are importable
- [ ] Pre-commit hooks are configured

## 🏷️ GitHub Configuration

### Labels to Create

Create these labels in your repository (Settings → Labels):

```bash
# Using GitHub CLI
gh label create "forge-intake" --color "0E8A16" --description "Request Intake v2 catalog generation"
gh label create "forge-stac" --color "1D76DB" --description "Request STAC catalog generation"
gh label create "forge-complete" --color "0E8A16" --description "Catalog generation completed"
gh label create "forge-failed" --color "D73A4A" --description "Catalog generation failed"
```

- [ ] `forge-intake` label exists
- [ ] `forge-stac` label exists
- [ ] `forge-complete` label exists
- [ ] `forge-failed` label exists

### Issue Templates

Visit `https://github.com/<owner>/<repo>/issues/new/choose` to verify:

- [ ] "Generate Intake v2 Catalog" template appears
- [ ] "Generate STAC Catalog" template appears
- [ ] Templates have correct fields and validation

### Workflows

Check Actions tab to verify:

- [ ] Workflows are present and not disabled
- [ ] No syntax errors in workflow files
- [ ] Workflow permissions are correct (`issues: write`, `contents: read`)

## 🧪 Testing

### Local Testing

```bash
# Test the parser can be executed
python .github/scripts/forge_parser.py --help || echo "Expected: requires env vars"

# Test the local tester
python tests/test_forge.py --help

# Install dependencies
pip install -e ".[intake,stac]"

# Run a local test (Intake)
python tests/test_forge.py intake \
  --uri "https://example.com/catalog.yaml" \
  --name "test" \
  --description "Test catalog"

# Run a local test (STAC)
python tests/test_forge.py stac \
  --uri "https://example.com/data.zarr" \
  --collection "test" \
  --project "TEST" \
  --description "Test collection"
```

- [ ] Local intake test works
- [ ] Local STAC test works
- [ ] Output appears in `forge_output/`

### CI Testing

Push changes and check:

- [ ] `test-forge.yml` workflow runs on push
- [ ] Tests pass for all Python versions
- [ ] Test artifacts are uploaded

### Real Issue Test

Create a test issue:

1. Go to Issues → New Issue
2. Select "Generate Intake v2 Catalog"
3. Fill with test data:
   ```
   Source URI: https://raw.githubusercontent.com/intake/intake/main/examples/catalog.yaml
   Output Name: test-catalog
   Source Type: Auto-detect
   Description: Test issue for forge verification
   ```
4. Submit issue

- [ ] Workflow triggers automatically
- [ ] Workflow completes (success or failure)
- [ ] Bot comments on issue with result
- [ ] Artifact is created
- [ ] Status label is applied
- [ ] Artifact can be downloaded

## 🔒 Security Review

- [ ] Workflow only triggers on specific labels
- [ ] No secrets or credentials in code
- [ ] Timeout limits are set
- [ ] File upload sizes are reasonable
- [ ] Error logs don't expose sensitive data

## 📚 Documentation Review

- [ ] README.md mentions forge prominently
- [ ] Quick start guide is clear and concise
- [ ] Examples cover common use cases
- [ ] Architecture doc explains system design
- [ ] All docs are linked properly

## 🚀 Production Readiness

### User Experience

- [ ] Issue templates are user-friendly
- [ ] Error messages are helpful
- [ ] Success criteria are clear
- [ ] Documentation is accessible

### Operational

- [ ] Monitoring plan in place (check issue labels)
- [ ] Error handling is comprehensive
- [ ] Logs are informative
- [ ] Artifact retention is appropriate (90 days)

### Performance

- [ ] Workflow runs in reasonable time (<10 min)
- [ ] Artifact sizes are manageable
- [ ] Concurrency limits are understood
- [ ] GitHub Actions minutes are tracked

## ✨ Optional Enhancements

Nice-to-have improvements:

- [ ] Custom GitHub Action for forge (instead of script)
- [ ] Workflow visualization in docs
- [ ] Usage statistics dashboard
- [ ] Email notifications for users
- [ ] Integration with project management tools
- [ ] Automated catalog validation
- [ ] Preview step before generation

## 🐛 Known Issues

Document any known limitations:

- STAC generator is currently a placeholder
- Only public URLs are supported
- No authentication for private data
- Limited to GitHub Actions concurrency
- Artifact size limited to 10GB

## 📞 Support Resources

- [ ] Document where users can get help
- [ ] Create discussion forum or channel
- [ ] Set up issue templates for forge bugs
- [ ] Provide contact information

## 🎯 Success Criteria

The forge is ready when:

1. ✅ All files are in place
2. ✅ Workflows run without errors
3. ✅ Issue templates work correctly
4. ✅ Local testing passes
5. ✅ Real issue test completes successfully
6. ✅ Documentation is complete
7. ✅ Team is trained on usage
8. ✅ Monitoring is in place

## 📝 Post-Launch

After deploying:

- [ ] Monitor first 10 issues closely
- [ ] Gather user feedback
- [ ] Track success/failure rates
- [ ] Measure execution times
- [ ] Identify common errors
- [ ] Update documentation based on feedback
- [ ] Create FAQ from common questions

## 🔄 Maintenance Schedule

Regular tasks:

- **Weekly:** Check failed forges, review errors
- **Monthly:** Update dependencies, review metrics
- **Quarterly:** Review and improve documentation
- **Yearly:** Major feature additions, architecture review

---

**Ready to go?** When all required items are checked, your forge is production-ready! 🚀
