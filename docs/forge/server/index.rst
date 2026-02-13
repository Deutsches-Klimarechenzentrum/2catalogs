.. Server-side: Git Continuous Integration (CI)

============================================
Server-side: Git Continuous Integration (CI)
============================================

The CI/CD workload is split between GitLab CI and GitHub Actions to optimize resources and leverage each platform's strengths.

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


.. toctree::
   :maxdepth: 4
   :caption: Platform Details

    CI_GITLAB