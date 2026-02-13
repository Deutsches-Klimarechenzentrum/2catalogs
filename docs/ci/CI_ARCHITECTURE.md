# Architecture - GitLab & GitHub Split

## Visual Overview

```mermaid
graph TB
    REPO["CODE REPOSITORY<br/>(Synced between platforms)"]
    
    REPO --> GH["GITHUB ACTIONS<br/>Testing & Quality"]
    REPO --> GL["GITLAB CI/CD<br/>Forge & Deploy"]
    
    GH --> TEST["Test Matrix<br/>• Python 3.9<br/>• Python 3.10<br/>• Python 3.11<br/>• Python 3.12"]
    GH --> LINT["Lint<br/>• Ruff<br/>• Code quality"]
    TEST --> BUILD["Build<br/>• Package building<br/>(main branch only)"]
    
    GL --> FORGE["Forge (Conda)<br/>• forge:intake<br/>• forge:stac<br/>• forge:all<br/>• forge:auto-commit"]
    GL --> DEPLOY["Deploy<br/>• GitLab Pages"]
    
    style REPO fill:#e1f5ff
    style GH fill:#fff3cd
    style GL fill:#d4edda
    style TEST fill:#f8f9fa
    style LINT fill:#f8f9fa
    style BUILD fill:#f8f9fa
    style FORGE fill:#f8f9fa
    style DEPLOY fill:#f8f9fa
```

## Trigger Flow

```mermaid
graph TB
    subgraph GH_TRIGGERS["GitHub Actions Triggers"]
        GH1["Push to main/develop"]
        GH2["Pull Request"]
        GH3["Manual workflow dispatch"]
    end
    
    subgraph GL_TRIGGERS["GitLab CI/CD Triggers"]
        GL1["Push to main (Pages)"]
        GL2["Manual pipeline run"]
        GL3["Webhook trigger (issues)"]
    end
    
    GH_TRIGGERS --> GH_EXEC["Automatic Testing<br/>• Runs on every PR<br/>• Fast feedback<br/>• Multiple versions"]
    GL_TRIGGERS --> GL_EXEC["Manual Forge Jobs<br/>• User initiated<br/>• On-demand<br/>• Conda environment"]
    
    style GH_TRIGGERS fill:#fff3cd
    style GL_TRIGGERS fill:#d4edda
    style GH_EXEC fill:#f8f9fa
    style GL_EXEC fill:#f8f9fa
```

## Job Dependencies

### GitHub Actions (Parallel)

```mermaid
graph LR
    PY39["test:python39"]
    PY310["test:python310"]
    PY311["test:python311"]
    PY312["test:python312"]
    LINT["lint"]
    BUILD["build (main only)"]
    
    PY39 --> RESULT1["✓ Pass/Fail"]
    PY310 --> RESULT1
    PY311 --> RESULT1
    PY312 --> RESULT1
    LINT --> RESULT2["✓ Pass/Fail"]
    BUILD --> ARTIFACT["✓ Package Artifact"]
    
    style PY39 fill:#fff3cd
    style PY310 fill:#fff3cd
    style PY311 fill:#fff3cd
    style PY312 fill:#fff3cd
    style LINT fill:#fff3cd
    style BUILD fill:#fff3cd
```

### GitLab CI/CD (Sequential)

```mermaid
graph TB
    INTAKE["forge:intake"]
    STAC["forge:stac"]
    ALL["forge:all"]
    PAGES["deploy:pages"]
    
    INTAKE -.->|manual| COMMIT["forge:auto-commit"]
    STAC -.->|manual| COMMIT
    ALL -.->|manual| COMMIT
    COMMIT --> REPO["commit to repo"]
    
    PAGES --> GITLAB["GitLab Pages"]
    
    style INTAKE fill:#d4edda
    style STAC fill:#d4edda
    style ALL fill:#d4edda
    style PAGES fill:#d4edda
```

## Runner Configuration

### GitHub Actions

```mermaid
graph TB
    GH["Standard GitHub<br/>Hosted Runners<br/><br/>• Ubuntu Latest<br/>• Python pre-installed<br/>• Fast boot time<br/>• Matrix-friendly"]
    
    style GH fill:#fff3cd
```

### GitLab CI/CD

```mermaid
graph TB
    GL["Custom Conda Runner<br/>(tags: [conda])<br/><br/>• Conda installed<br/>• Env: catalog-forge<br/>• Python 3.11<br/>• Project deps cached"]
    
    style GL fill:#d4edda
```

## Data Flow

### Testing Flow (GitHub)

```mermaid
graph LR
    DEV["Developer"] --> PUSH["Push/PR"]
    PUSH --> GH["GitHub"]
    GH --> MATRIX["Test Matrix"]
    MATRIX --> RESULTS["Results"]
    RESULTS --> STATUS["PR Status"]
    MATRIX --> REPORTS["Test Reports"]
    MATRIX --> COVERAGE["Coverage Data"]
    MATRIX --> ARTIFACTS["Build Artifacts"]
    
    style DEV fill:#e1f5ff
    style MATRIX fill:#fff3cd
```

### Forge Flow (GitLab)

```mermaid
graph TB
    USER["User"] --> TRIGGER["Manual Trigger"]
    TRIGGER --> VARS["Variables<br/>• CATALOG_TYPE<br/>• ISSUE_BODY<br/>• ISSUE_NUMBER"]
    TRIGGER --> GL["GitLab"]
    GL --> FORGE["Forge Job"]
    FORGE --> CAT["Catalog Generated"]
    FORGE --> ART["Artifacts<br/>forge_output/"]
    CAT --> COMMIT["(Optional) Auto-commit"]
    COMMIT --> REPO["Updated Repository"]
    
    style USER fill:#e1f5ff
    style FORGE fill:#d4edda
```

## Pipeline Complexity Comparison

### Before Split

```mermaid
graph TB
    subgraph GITLAB_BEFORE["GitLab CI: ~490 lines"]
        GL_LINT["lint (2 jobs)"]
        GL_TEST["test (5+ jobs)"]
        GL_BUILD["build (2 jobs)"]
        GL_FORGE["forge (4 jobs)"]
        GL_DEPLOY["deploy (3 jobs)"]
        GL_NOTIFY["notify (2 jobs)"]
    end
    
    subgraph GITHUB_BEFORE["GitHub CI: ~164 lines"]
        GH_TEST["test (1 job)"]
        GH_FORGE["test-forge (1 job)"]
        GH_LINT["lint (1 job)"]
    end
    
    subgraph GH_FORGE_WF["GitHub Forge: ~260 lines"]
        PARSE["parse-and-forge (issue-triggered)"]
    end
    
    TOTAL["Total: 18+ jobs across 6 stages (GitLab)<br/>+ 3 jobs (GitHub CI)<br/>+ issue workflow"]
    
    GITLAB_BEFORE --> TOTAL
    GITHUB_BEFORE --> TOTAL
    GH_FORGE_WF --> TOTAL
```

### After Split

```mermaid
graph TB
    subgraph GITLAB_AFTER["GitLab CI: ~187 lines (62% reduction) ✓"]
        GL_FORGE2["forge (4 jobs)"]
        GL_DEPLOY2["deploy (1 job)"]
        GL_NOTE["All jobs use conda runner"]
    end
    
    subgraph GITHUB_AFTER["GitHub CI: ~135 lines (18% reduction) ✓"]
        GH_TEST2["test (1 matrix job, 4 versions)"]
        GH_LINT2["lint (1 job)"]
        GH_BUILD2["build (1 job)"]
    end
    
    subgraph GH_FORGE_DISABLED["GitHub Forge: ~259 lines (DISABLED) ✓"]
        DISABLED["All jobs set to if: false"]
    end
    
    RESULT["Total: 5 jobs (GitLab) + 3 jobs (GitHub)<br/>Focused & Optimized"]
    
    GITLAB_AFTER --> RESULT
    GITHUB_AFTER --> RESULT
    GH_FORGE_DISABLED -.->|disabled| RESULT
    
    style GITLAB_AFTER fill:#d4edda
    style GITHUB_AFTER fill:#fff3cd
    style GH_FORGE_DISABLED fill:#f8d7da
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

| Task | GitHub | GitLab |
|------|--------|--------|
| Python Testing | ✅ | ❌ |
| Multi-version Test | ✅ | ❌ |
| Code Linting | ✅ | ❌ |
| Package Building | ✅ | ❌ |
| Catalog Generation | ❌ | ✅ |
| Manual Forge Jobs | ❌ | ✅ |
| Auto-commit | ❌ | ✅ |
| Pages Deployment | ❌ | ✅ |
| Issue Automation | ❌ | ✅ |
| Conda Environment | ❌ | ✅ |

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
