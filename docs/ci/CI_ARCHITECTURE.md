# CI/CD Architecture - GitLab & GitHub Split

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CODE REPOSITORY                          │
│                     (Synced between platforms)                   │
└─────────────────────────────────────────────────────────────────┘
                    │                          │
                    ▼                          ▼
        ┌───────────────────────┐  ┌───────────────────────┐
        │   GITHUB ACTIONS      │  │   GITLAB CI/CD        │
        │   Testing & Quality   │  │   Forge & Deploy      │
        └───────────────────────┘  └───────────────────────┘
                    │                          │
                    │                          │
        ┌───────────▼───────────┐  ┌───────────▼───────────┐
        │                       │  │                       │
        │   Test (Matrix)       │  │   Forge (Conda)       │
        │   • Python 3.9        │  │   • forge:intake      │
        │   • Python 3.10       │  │   • forge:stac        │
        │   • Python 3.11       │  │   • forge:all         │
        │   • Python 3.12       │  │   • forge:auto-commit │
        │                       │  │                       │
        └───────────┬───────────┘  └───────────┬───────────┘
                    │                          │
        ┌───────────▼───────────┐  ┌───────────▼───────────┐
        │                       │  │                       │
        │   Lint                │  │   Deploy              │
        │   • Ruff              │  │   • GitLab Pages      │
        │   • Code quality      │  │                       │
        │                       │  │                       │
        └───────────┬───────────┘  └───────────────────────┘
                    │
        ┌───────────▼───────────┐
        │                       │
        │   Build               │
        │   • Package building  │
        │   (main branch only)  │
        │                       │
        └───────────────────────┘
```

## Trigger Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                           TRIGGERS                               │
└─────────────────────────────────────────────────────────────────┘

GitHub Actions Triggers:                   GitLab CI/CD Triggers:
├── Push to main/develop                  ├── Push to main (Pages)
├── Pull Request                          ├── Manual pipeline run
└── Manual workflow dispatch              └── Webhook trigger (issues)

        │                                          │
        ▼                                          ▼
┌─────────────────────┐               ┌─────────────────────┐
│ Automatic Testing   │               │ Manual Forge Jobs   │
│ • Runs on every PR  │               │ • User initiated    │
│ • Fast feedback     │               │ • On-demand         │
│ • Multiple versions │               │ • Conda environment │
└─────────────────────┘               └─────────────────────┘
```

## Job Dependencies

### GitHub Actions (Parallel)
```
test:python39  ┐
test:python310 ├─── (parallel) ──> ✓ Pass/Fail
test:python311 │
test:python312 ┘

lint ──────────────────────────> ✓ Pass/Fail

build (main only) ─────────────> ✓ Package Artifact
```

### GitLab CI/CD (Sequential)
```
forge:intake  ┐
forge:stac    ├─── (manual, one at a time) ──> forge:auto-commit
forge:all     ┘                                      │
                                                     ▼
                                              (commit to repo)

deploy:pages ──────────────────────────────> GitLab Pages
```

## Runner Configuration

### GitHub Actions
```
┌─────────────────────────┐
│   Standard GitHub       │
│   Hosted Runners        │
│                         │
│   • Ubuntu Latest       │
│   • Python pre-installed│
│   • Fast boot time      │
│   • Matrix-friendly     │
└─────────────────────────┘
```

### GitLab CI/CD
```
┌─────────────────────────┐
│   Custom Conda Runner   │
│   (tags: [conda])       │
│                         │
│   • Conda installed     │
│   • Env: catalog-forge  │
│   • Python 3.11         │
│   • Project deps cached │
└─────────────────────────┘
```

## Data Flow

### Testing Flow (GitHub)
```
Developer → Push/PR → GitHub → Test Matrix → Results → PR Status
                                    │
                                    ├─> Test Reports
                                    ├─> Coverage Data
                                    └─> Build Artifacts
```

### Forge Flow (GitLab)
```
User → Manual Trigger → GitLab → Forge Job → Catalog Generated
           │                          │
           ├─> Variables              ├─> Artifacts
           │   • CATALOG_TYPE         └─> forge_output/
           │   • ISSUE_BODY
           └─> ISSUE_NUMBER
                                           │
                                           ▼
                                    (Optional) Auto-commit
                                           │
                                           ▼
                                    Updated Repository
```

## Pipeline Complexity Comparison

### Before Split
```
GitLab CI: ~490 lines
├── lint (2 jobs)
├── test (5+ jobs)
├── build (2 jobs)
├── forge (4 jobs)
├── deploy (3 jobs)
└── notify (2 jobs)
Total: 18+ jobs across 6 stages

GitHub CI: ~164 lines
├── test (1 job)
├── test-forge (1 job)
└── lint (1 job)
Total: 3 jobs

GitHub Forge: ~260 lines
└── parse-and-forge (issue-triggered)
```

### After Split
```
GitLab CI: ~187 lines (62% reduction) ✓
├── forge (4 jobs)
└── deploy (1 job)
Total: 5 jobs across 2 stages
All jobs use conda runner

GitHub CI: ~135 lines (18% reduction) ✓
├── test (1 matrix job, 4 versions)
├── lint (1 job)
└── build (1 job)
Total: 3 jobs

GitHub Forge: ~259 lines (DISABLED) ✓
└── All jobs set to if: false
```

## Resource Usage Estimate

### Before
```
GitHub Actions:
├── Test matrix: ~10 min × 4 = 40 min
├── Forge testing: ~5 min
└── Lint: ~2 min
Total per run: ~47 minutes

GitLab CI:
├── All stages: ~30-40 min
Total per run: ~35 minutes

Combined: ~82 minutes per full run
```

### After
```
GitHub Actions:
├── Test matrix: ~10 min × 4 = 40 min
├── Lint: ~2 min
└── Build: ~3 min
Total per run: ~45 minutes (5% reduction)

GitLab CI:
├── Forge (manual): ~5-10 min
└── Deploy: ~1 min
Total per run: ~6-11 minutes (70% reduction)

Combined: ~51-56 minutes
Overall savings: ~30-35%
```

## Responsibility Matrix

```
┌────────────────────┬──────────────┬──────────────┐
│      Task          │   GitHub     │   GitLab     │
├────────────────────┼──────────────┼──────────────┤
│ Python Testing     │      ✅      │      ❌      │
│ Multi-version Test │      ✅      │      ❌      │
│ Code Linting       │      ✅      │      ❌      │
│ Package Building   │      ✅      │      ❌      │
│ Catalog Generation │      ❌      │      ✅      │
│ Manual Forge Jobs  │      ❌      │      ✅      │
│ Auto-commit        │      ❌      │      ✅      │
│ Pages Deployment   │      ❌      │      ✅      │
│ Issue Automation   │      ❌      │      ✅      │
│ Conda Environment  │      ❌      │      ✅      │
└────────────────────┴──────────────┴──────────────┘
```

## Configuration Files

```
Repository Root
├── .github/
│   └── workflows/
│       ├── ci.yml              (Testing & Quality - Active)
│       └── forge-catalog.yml   (DISABLED - Notice only)
│
├── .gitlab/
│   ├── scripts/
│   │   └── forge_parser.py     (Forge parser for GitLab)
│   └── ...documentation...
│
├── .gitlab-ci.yml              (Forge & Deploy - Active)
│
└── Documentation
    ├── CI_SPLIT_GUIDE.md
    ├── CI_SPLIT_SUMMARY.md
    └── CI_ARCHITECTURE.md (this file)
```

## Environment Setup

### GitHub Actions Environment
```yaml
Environment: ubuntu-latest
Python: 3.9, 3.10, 3.11, 3.12 (matrix)
Package Manager: pip
Cache: pip cache
Dependencies: Installed per job
Setup Time: ~30 seconds
```

### GitLab CI/CD Environment  
```yaml
Environment: Custom runner with conda
Python: 3.11 (via conda)
Package Manager: conda + pip
Cache: Conda environment
Dependencies: Pre-installed in conda env
Setup Time: ~10 seconds (env exists) or ~2 min (first time)
Tag Required: conda
```

## Success Criteria

✅ **Separation Achieved**
- GitHub handles all testing
- GitLab handles all forge operations
- No overlap or duplication

✅ **Performance Optimized**
- 62% reduction in GitLab pipeline size
- 18% reduction in GitHub pipeline size
- ~30% overall time savings

✅ **Conda Integration**
- All GitLab jobs use conda runner
- Single Python 3.11 environment
- Consistent dependency management

✅ **Documentation Complete**
- Split guide created
- Summary documented
- Architecture visualized

✅ **Backward Compatible**
- GitHub testing unchanged for users
- Forge moved to GitLab with clear instructions
- No breaking changes for contributors

---

**Architecture Version**: 1.0  
**Last Updated**: February 6, 2026  
**Status**: ✅ Production Ready
