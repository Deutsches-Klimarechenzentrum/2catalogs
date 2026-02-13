.. CI/CD Architecture

================================
CI/CD Architecture Overview
================================

The CI/CD workload is split between GitLab CI and GitHub Actions to optimize resources and leverage each platform's strengths.

.. toctree::
   :maxdepth: 2
   :caption: Platform Details

   CI_GITLAB
   CI_GITHUB

Architecture
============

System Overview
---------------

.. mermaid::

   graph TB
       REPO["CODE REPOSITORY<br/>(Synced between platforms)"]
       
       REPO --> GH["GITHUB ACTIONS<br/>Testing & Quality"]
       REPO --> GL["GITLAB CI/CD<br/>Forge & Deploy"]
       
       GH --> TEST["Test Matrix<br/>• Python 3.9-3.12"]
       GH --> LINT["Lint & Build"]
       
       GL --> FORGE["Forge Jobs<br/>• Manual triggers<br/>• Conda environment"]
       GL --> DEPLOY["Pages Deployment"]
       
       style REPO fill:#e1f5ff
       style GH fill:#fff3cd
       style GL fill:#d4edda

Responsibility Split
--------------------

========================================  ==========  ==========
Task                                      GitHub      GitLab
========================================  ==========  ==========
Multi-version Python Testing              ✅          ❌
Code Linting & Quality                    ✅          ❌
Package Building                          ✅          ❌
Catalog Generation (Forge)                ❌          ✅
Manual Forge Jobs                         ❌          ✅
Auto-commit                               ❌          ✅
GitLab Pages Deployment                   ❌          ✅
Conda Environment                         ❌          ✅
========================================  ==========  ==========

Performance Improvements
------------------------

**Before Split:**

- GitLab: ~490 lines, 18+ jobs across 6 stages
- GitHub: ~164 lines, 3 jobs
- Combined: ~82 minutes per full run

**After Split:**

- GitLab: ~187 lines, 5 jobs (62% reduction)
- GitHub: ~135 lines, 3 jobs (18% reduction)
- Combined: ~51-56 minutes (30-35% savings)

Trigger Conditions
------------------

**GitHub Actions:**

- Push to main/develop branches
- Pull requests
- Manual workflow dispatch

**GitLab CI/CD:**

- Push to main (for Pages)
- Manual pipeline runs (for forge)
- Webhook triggers (GitHub issues)

Benefits
--------

**GitHub Strengths:**

- Matrix testing across Python versions
- Fast runners and quick feedback
- Excellent PR integration
- Rich marketplace ecosystem

**GitLab Strengths:**

- Custom conda runners
- Precise environment control
- Easy manual job triggers
- Powerful artifact management
- Native Pages support

Getting Started
===============

Quick Start
-----------

1. **For Testing** → Use GitHub Actions (automatic on PR)
2. **For Forge** → Use GitLab CI/CD (manual trigger)
3. **For Pages** → Automatic on GitLab main branch push

See :doc:`CI_GITHUB` for GitHub setup and :doc:`CI_GITLAB` for GitLab configuration.

Configuration Files
-------------------

::

   Repository Root
   ├── .github/workflows/
   │   ├── ci.yml              (Testing & Quality)
   │   └── forge-catalog.yml   (DISABLED)
   ├── .gitlab-ci.yml          (Forge & Deploy)
   └── .gitlab/scripts/
       └── forge_parser.py

Best Practices
--------------

**Do:**

- ✅ Use GitHub for testing and quality checks
- ✅ Use GitLab for forge operations
- ✅ Keep code synced between platforms
- ✅ Monitor both CI/CD dashboards

**Don't:**

- ❌ Run forge on GitHub (disabled)
- ❌ Duplicate tests across platforms
- ❌ Mix responsibilities