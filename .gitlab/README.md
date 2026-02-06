# GitLab Configuration

This directory contains GitLab-specific configuration files for the 2catalogs project.

## Contents

### 📁 Directory Structure

```
.gitlab/
├── README.md                          # This file
├── GITLAB_CONFIGURATION.md            # Detailed CI/CD configuration guide
├── MIGRATION_GUIDE.md                 # GitHub to GitLab migration guide
├── issue_templates/                   # Issue templates
│   ├── Bug_Report.md
│   ├── Feature_Request.md
│   ├── Forge_Intake.md
│   ├── Forge_STAC.md
│   └── Forge_All.md
├── merge_request_templates/           # MR templates
│   └── default.md
└── scripts/                           # GitLab CI/CD scripts
    └── forge_parser.py                # Catalog generation parser
```

---

## Quick Links

- 📖 **[Configuration Guide](GITLAB_CONFIGURATION.md)** - Complete CI/CD setup instructions
- 🚀 **[Migration Guide](MIGRATION_GUIDE.md)** - Step-by-step GitHub to GitLab migration
- 🔧 **[Main CI/CD Config](../.gitlab-ci.yml)** - Pipeline configuration file

---

## Getting Started

### 1. First Time Setup

If this is your first time setting up GitLab for this project:

1. **Read the [Migration Guide](MIGRATION_GUIDE.md)** if migrating from GitHub
2. **Follow the [Configuration Guide](GITLAB_CONFIGURATION.md)** to:
   - Replace placeholders in `.gitlab-ci.yml`
   - Set up required CI/CD variables
   - Configure deployment targets
3. **Test the pipeline** with a manual run
4. **Set up issue templates** (automatically available)
5. **Configure GitLab Pages** (if needed)

### 2. Quick Configuration

**Minimum required configuration**:

```yaml
# In .gitlab-ci.yml, replace these placeholders:
<DOCKER_IMAGE>         → python:3.11-slim
<GITLAB_REGISTRY>      → registry.gitlab.com/<namespace>/<project>
<PAGES_BRANCH>         → main
<ENVIRONMENT_NAME>     → production
<DEPLOY_URL>           → https://<namespace>.gitlab.io/<project>
```

**Minimum required CI/CD variables** (Settings > CI/CD > Variables):
- `CI_PUSH_TOKEN`: Personal access token with `write_repository` scope

### 3. Verify Setup

Run this checklist:

- [ ] `.gitlab-ci.yml` placeholders replaced
- [ ] `CI_PUSH_TOKEN` variable set
- [ ] Pipeline runs successfully
- [ ] At least one test job passes
- [ ] Scripts are executable (`chmod +x .gitlab/scripts/*`)

---

## Issue Templates

### Available Templates

Located in `.gitlab/issue_templates/`:

1. **Bug_Report.md** - Report bugs or unexpected behavior
2. **Feature_Request.md** - Suggest new features
3. **Forge_Intake.md** - Request Intake catalog generation
4. **Forge_STAC.md** - Request STAC catalog generation  
5. **Forge_All.md** - Request both Intake and STAC catalogs

### Using Issue Templates

1. Go to **Issues > New issue**
2. Optional: Click "Choose a template" dropdown
3. Select the appropriate template
4. Fill in the form fields
5. Add relevant labels (e.g., `forge-intake`, `bug`)
6. Submit the issue

### Setting Default Template

To set a default issue template:

1. Go to **Settings > General**
2. Expand "Default issue template"
3. Select: `.gitlab/issue_templates/Bug_Report.md`
4. Save changes

---

## Merge Request Templates

### Default Template

The default MR template is automatically applied to new merge requests.

Location: `.gitlab/merge_request_templates/default.md`

**Includes**:
- Change description
- Type of change checklist
- Related issues
- Testing information
- Review checklist
- Screenshots/output section

### Using MR Templates

Templates are automatically applied when creating an MR. You can also:

1. Create MR normally
2. In the description, add: `/label ~needs-review`
3. The template is auto-populated

### Custom MR Templates

To create additional templates:

1. Add new file: `.gitlab/merge_request_templates/your_template.md`
2. When creating MR, select from "Choose a template" dropdown

---

## CI/CD Pipeline

### Pipeline Stages

The GitLab CI/CD pipeline has 6 stages:

1. **Lint** - Code quality checks
2. **Test** - Run tests on multiple Python versions
3. **Build** - Build packages and Docker images
4. **Forge** - Manual catalog generation jobs
5. **Deploy** - Deploy to Pages, S3, or registries
6. **Notify** - Send notifications (Slack, email)

### Configuration

**Pipeline configuration**: [`../.gitlab-ci.yml`](../.gitlab-ci.yml)

**Key features**:
- ✅ Multi-version Python testing (3.9-3.12)
- ✅ Code coverage reporting
- ✅ Docker image building
- ✅ Manual forge jobs
- ✅ GitLab Pages deployment
- ✅ S3 deployment
- ✅ PyPI publishing
- ✅ Artifact management
- ✅ Notifications

### Running Pipelines

**Automatic triggers**:
- Push to `main` or `develop`
- Merge requests
- Git tags
- Scheduled runs

**Manual trigger**:
1. Go to **CI/CD > Pipelines**
2. Click "Run pipeline"
3. Select branch
4. Add variables (for forge jobs)
5. Click "Run pipeline"

### Viewing Pipeline Results

1. Go to **CI/CD > Pipelines**
2. Click on a pipeline to see all jobs
3. Click on a job to see its log
4. Download artifacts from the job page

---

## Forge System

### What is Forge?

The Forge system automatically generates data catalogs (Intake v2 and STAC) from user requests.

### Manual Forge Jobs

Three manual jobs are available:

1. **`forge:intake`** - Generate Intake v2 catalog
2. **`forge:stac`** - Generate STAC catalog
3. **`forge:all`** - Generate both catalog types

### Running a Forge Job

#### Method 1: Via Pipeline

1. Go to **CI/CD > Pipelines > Run pipeline**
2. Set variables:
   ```
   CATALOG_TYPE: intake  # or stac, or all
   ISSUE_BODY: <paste issue template content>
   ISSUE_NUMBER: manual-001
   ```
3. Click "Run pipeline"
4. In pipeline view, click play (▶️) on the forge job
5. Download artifacts after completion

#### Method 2: Via Issue (Future)

Create an issue using forge templates:
- Use `.gitlab/issue_templates/Forge_Intake.md`
- Fill in the required fields
- Add label: `forge-intake` or `forge-stac`
- (Requires additional webhook configuration)

### Forge Output

Generated files are saved as pipeline artifacts in `forge_output/`:
- `info.txt` - Generation details
- `*.yaml` - Generated Intake catalogs
- `*.json` - Generated STAC collections
- `error.log` - Error details (if failed)
- `duplicate_warning.txt` - Duplicate warnings (if applicable)

### Artifacts

**Retention**: 90 days (configurable)

**Download**:
1. Go to job page
2. Click "Browse" or "Download" on the right
3. Access individual files or download entire artifact

---

## Scripts

### forge_parser.py

**Location**: `.gitlab/scripts/forge_parser.py`

**Purpose**: Parse issue body or manual input and generate catalogs

**Usage**:
```bash
# Set environment variables
export ISSUE_BODY="<issue template content>"
export ISSUE_NUMBER="123"
export CATALOG_TYPE="intake"  # or stac, or all

# Run the parser
python .gitlab/scripts/forge_parser.py
```

**Requirements**:
- Python 3.9+
- Dependencies from `pyproject.toml` installed
- Access to source catalogs/data

**Permissions**:
```bash
# Make executable (if needed)
chmod +x .gitlab/scripts/forge_parser.py
```

---

## Configuration Reference

### Placeholders in .gitlab-ci.yml

All placeholders are marked with `<PLACEHOLDER_NAME>`. See [GITLAB_CONFIGURATION.md](GITLAB_CONFIGURATION.md) for complete list.

**Essential placeholders**:
- `<DOCKER_IMAGE>` - Base Docker image
- `<GITLAB_REGISTRY>` - Container registry URL
- `<PAGES_BRANCH>` - Branch for GitLab Pages
- `<DEPLOY_URL>` - Deployment URL

### CI/CD Variables Reference

**Required for full functionality**:

| Variable | Purpose | Required |
|----------|---------|----------|
| `CI_PUSH_TOKEN` | Push access to repository | ✅ |
| `AWS_ACCESS_KEY_ID` | AWS S3 access | For S3 deploy |
| `AWS_SECRET_ACCESS_KEY` | AWS S3 secret | For S3 deploy |
| `PYPI_TOKEN` | PyPI publishing | For releases |
| `SLACK_WEBHOOK_URL` | Slack notifications | Optional |
| `STAC_API_KEY` | STAC API access | For STAC API |

**Set in**: Settings > CI/CD > Variables

**Best practices**:
- ✅ Mark secrets as "Masked"
- ✅ Mark production secrets as "Protected"
- ✅ Use minimal required scopes
- ✅ Set expiration dates on tokens
- ✅ Document variable purpose

---

## Troubleshooting

### Common Issues

#### Pipeline Won't Start
- **Check**: CI/CD enabled (Settings > General > Visibility)
- **Check**: `.gitlab-ci.yml` syntax (CI/CD > Editor > Validate)
- **Check**: Runner available (Settings > CI/CD > Runners)

#### Job Fails Immediately
- **Check**: Docker image exists and is accessible
- **Check**: Script file permissions (`chmod +x`)
- **Check**: Required CI/CD variables are set

#### Forge Job Fails
- **Check**: `ISSUE_BODY` format matches template
- **Check**: All required fields present
- **Check**: Dependencies installed in job
- **Review**: `forge_output/error.log` in artifacts

#### Deployment Fails
- **Pages**: Ensure `public/` directory created
- **S3**: Verify AWS credentials and permissions
- **PyPI**: Check token validity and package name

### Getting Help

1. **Check logs**: CI/CD > Pipelines > Select pipeline > Click job
2. **Review guides**: [GITLAB_CONFIGURATION.md](GITLAB_CONFIGURATION.md)
3. **Validate config**: CI/CD > Editor > Validate
4. **Open issue**: Create issue with details
5. **GitLab docs**: https://docs.gitlab.com/ee/ci/

---

## Best Practices

### Security

- ✅ **Never commit secrets** - Use CI/CD variables
- ✅ **Mask sensitive variables** - Mark as "Masked"
- ✅ **Protect production variables** - Mark as "Protected"
- ✅ **Use minimal scopes** - Limit token permissions
- ✅ **Rotate tokens regularly** - Set expiration dates
- ✅ **Review pipeline logs** - Check for leaked secrets

### Performance

- ✅ **Use cache** - Cache dependencies between jobs
- ✅ **Parallelize tests** - Run tests concurrently
- ✅ **Optimize images** - Use slim/alpine images
- ✅ **Limit artifacts** - Set appropriate retention
- ✅ **Clean up** - Remove old branches/artifacts

### Maintenance

- ✅ **Monitor pipelines** - Check for failures
- ✅ **Update dependencies** - Keep images current
- ✅ **Review artifacts** - Clean up old artifacts
- ✅ **Update docs** - Keep guides current
- ✅ **Test changes** - Use merge requests

---

## Additional Resources

### Documentation

- **[GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)** - Official documentation
- **[GitLab CI/CD Examples](https://docs.gitlab.com/ee/ci/examples/)** - Example configurations
- **[GitLab API](https://docs.gitlab.com/ee/api/)** - Automation API
- **[GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/)** - Pages documentation

### Project Documentation

- **[Configuration Guide](GITLAB_CONFIGURATION.md)** - Detailed setup instructions
- **[Migration Guide](MIGRATION_GUIDE.md)** - GitHub to GitLab migration
- **[Main README](../README.md)** - Project overview
- **[Setup Guide](../SETUP_GUIDE.md)** - Installation instructions

### Community

- **[GitLab Forum](https://forum.gitlab.com/)** - Community discussions
- **[GitLab Discord](https://discord.gg/gitlab)** - Real-time chat
- **[GitLab Twitter](https://twitter.com/gitlab)** - Updates and news

---

## Contributing

### Improving GitLab Configuration

To improve the GitLab setup:

1. **Create a merge request** with your changes
2. **Update documentation** if configuration changes
3. **Test the pipeline** to ensure it still works
4. **Request review** from maintainers

### Reporting Issues

Found a problem?

1. **Check existing issues**: Issues > Search
2. **Create new issue**: Use "Bug Report" template
3. **Include details**:
   - What you expected
   - What actually happened
   - Pipeline/job logs
   - Configuration (sanitized)

---

## Changelog

### Version History

**v1.0.0** (2026-02-06)
- Initial GitLab configuration
- CI/CD pipeline with 6 stages
- Issue and MR templates
- Forge automation system
- Comprehensive documentation
- Migration guide from GitHub

---

## License

Same license as the main project. See [LICENSE](../LICENSE) for details.

---

## Contact

For questions or support:
- **Create an issue**: [Project Issues](../../issues)
- **Check docs**: [GITLAB_CONFIGURATION.md](GITLAB_CONFIGURATION.md)
- **Contact maintainers**: See project members

---

**Last Updated**: February 6, 2026  
**Maintained By**: Project maintainers  
**Version**: 1.0.0
