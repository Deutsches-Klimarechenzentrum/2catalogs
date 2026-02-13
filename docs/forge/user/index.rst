.. Forge User Guide

=====================
Forge User Guide
=====================

The Forge system automatically generates catalogs through GitHub Issues. No installation required!

.. contents:: Table of Contents
   :local:
   :depth: 2

Quick Start
===========

3-Step Process
--------------

**Step 1: Create Issue**

Go to GitHub Issues and select your catalog type:

- 🔄 **Generate Intake v2 Catalog** - Convert Intake v1, Zarr, or Parquet to Intake v2
- 🗺️ **Generate STAC Catalog** - Create STAC catalogs from Earth System Model data

**Step 2: Fill the Form**

For Intake v2::

   Source URI: https://your-catalog-url/catalog.yaml
   Output Name: my-catalog-v2
   Source Type: Intake v1 YAML Catalog

For STAC::

   Data Source: https://your-data-url/dataset.zarr
   Collection ID: my-collection
   Project ID: MY-PROJECT
   Description: My awesome dataset

**Step 3: Download Results**

1. Wait for the bot to comment (~2-5 minutes)
2. Click the Actions link in the comment
3. Download the ``catalog-issue-XXX`` artifact
4. Extract and use your catalog!

The forge will automatically:

✅ Validate your inputs
✅ Run the catalog generator
✅ Create a downloadable artifact
✅ Comment on your issue with results
✅ Create a merge request in GitLab (if configured)

Catalog Types
=============

Intake v2 Catalogs
------------------

**Use case:** Convert existing catalogs or data stores to Intake v2 format

**Required fields:**

- **Source URI** - URL or path to input
- **Output Catalog Name** - Name for the generated catalog  
- **Source Type** - Type of input (Intake v1, Zarr, Parquet, or Auto-detect)

**Example:**

.. code-block:: yaml

   Source URI: https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml
   Output Name: hackathon-intake-v2
   Source Type: Intake v1 YAML Catalog
   Description: Digital Earth's Global Hackathon catalog converted to Intake v2

STAC Catalogs
-------------

**Use case:** Generate STAC collections from Earth System Model output

**Required fields:**

- **Data Source URI** - URL or path to the dataset
- **Collection ID** - Unique identifier for the collection
- **Project ID** - Project identifier (e.g., EERIE, NextGEMS)
- **Description** - Detailed description of the dataset

**Example:**

.. code-block:: yaml

   Data Source: https://example.com/data/icon-ngc4008.zarr
   Collection ID: eerie-icon-ngc4008
   Project ID: EERIE
   Source ID: ICON
   Experiment ID: ngc4008
   Description: ICON high-resolution atmospheric data from the EERIE project

Examples
========

Example 1: Convert Public Catalog
----------------------------------

**Scenario:** Convert a public Intake v1 catalog to v2

1. Create issue with "Generate Intake v2 Catalog" template
2. Fill in::

      Source URI: https://digital-earths-global-hackathon.github.io/catalog/online/catalog.yaml
      Output Name: hackathon-intake-v2
      Source Type: Intake v1 YAML Catalog

3. Submit and wait ~2-5 minutes
4. Download artifact containing:
   
   - ``hackathon-intake-v2.yaml`` - Converted catalog
   - ``info.txt`` - Generation metadata
   - Log files

Example 2: Generate STAC Collection
------------------------------------

**Scenario:** Create STAC collection for EERIE model data

1. Create issue with "Generate STAC Catalog" template
2. Fill in::

      Data Source: https://s3.dkrz.de/my-bucket/eerie/icon-ngc4008.zarr
      Collection ID: eerie-icon-ngc4008
      Project ID: EERIE
      Source ID: ICON
      Description: High-resolution ICON atmospheric model output

3. Submit and download the STAC collection JSON

Example 3: Local Testing
-------------------------

Test the forge locally before creating an issue:

.. code-block:: bash

   # Install dependencies
   pip install -e ".[intake]"

   # Test intake conversion
   python tests/test_forge.py intake \\
     --uri "https://example.com/catalog.yaml" \\
     --name "test-catalog" \\
     --description "Test conversion"

   # Check output
   ls forge_output/
   cat forge_output/info.txt

Example 4: Batch Processing
----------------------------

Process multiple catalogs:

1. Create one issue per catalog
2. Use consistent naming
3. Add custom label for batch tracking (e.g., ``batch-2024-02``)
4. Monitor progress::

      gh issue list --label "forge-intake,batch-2024-02"
      gh issue list --label "forge-complete,batch-2024-02"

Labels
======

The forge uses these labels automatically:

- **forge-intake** - Triggers Intake v2 catalog generation
- **forge-stac** - Triggers STAC catalog generation  
- **forge-complete** - Added when generation succeeds
- **forge-failed** - Added when generation fails

Artifacts
=========

After completion:

- **Location:** Actions tab → Workflow run → Artifacts
- **Name:** ``catalog-issue-<number>``
- **Retention:** 90 days
- **Contents:** Generated catalogs, logs, metadata

Troubleshooting
===============

Common Issues
-------------

**"Source URI not accessible"**

- Verify URL is publicly accessible
- Test URL in browser first
- Ensure no authentication required

**"Timeout after 10 minutes"**

- Split large catalogs into smaller chunks
- Use ``reference::`` format for large datasets
- Contact maintainers for timeout increase

**"Invalid YAML format"**

- Validate source catalog syntax
- Check for special characters in strings
- Ensure proper indentation

Debugging
---------

If the forge fails:

1. Check the error comment on your issue
2. View full logs in Actions tab
3. Verify inputs match required format
4. Try test command locally to reproduce
5. Check data accessibility

Local Testing
=============

Test locally before creating issues:

.. code-block:: bash

   # Set up environment
   export CATALOG_TYPE="intake"
   export ISSUE_NUMBER="test"
   export ISSUE_BODY="### Source URI
   https://example.com/catalog.yaml
   
   ### Output Catalog Name
   my-catalog"

   # Run the parser
   python .github/scripts/forge_parser.py

   # Check output
   ls forge_output/

Setup Checklist
===============

For administrators setting up the forge:

Required Files
--------------

☐ ``.github/workflows/forge-catalog.yml`` exists
☐ ``.github/ISSUE_TEMPLATE/forge-intake.yml`` exists
☐ ``.github/ISSUE_TEMPLATE/forge-stac.yml`` exists
☐ ``.github/scripts/forge_parser.py`` exists
☐ ``.gitlab/scripts/forge_parser.py`` exists (for GitLab integration)

GitHub Labels
-------------

Create these labels in Settings → Labels:

☐ ``forge-intake`` (color: ``0E8A16``)
☐ ``forge-stac`` (color: ``1D76DB``)
☐ ``forge-complete`` (color: ``0E8A16``)
☐ ``forge-failed`` (color: ``D73A4A``)

Verification
------------

☐ Issue templates appear at ``github.com/<owner>/<repo>/issues/new/choose``
☐ Workflows are enabled in Actions tab
☐ Test issue completes successfully
☐ Artifacts download correctly

Advanced Features
=================

Custom Options
--------------

For Intake catalogs, pass additional options::

   --log-level DEBUG
   --include-pattern '*.zarr'

STAC Templates
--------------

For STAC generation:

- Use EERIE Cloud templates (checkbox)
- Generate preview thumbnails (checkbox)
- Include Kerchunk references (checkbox)

GitLab Integration
------------------

When configured, the forge will:

1. Generate catalog via GitHub Actions
2. Create merge request in GitLab
3. Post MR link to GitHub issue
4. Allow review before merging

See :doc:`../server/index` for CI/CD configuration.

Limitations
===========

- **Artifact size:** 10GB maximum
- **Retention:** 90 days
- **Timeout:** 10 minutes per command, 60 minutes total
- **Access:** Input URIs must be publicly accessible

Best Practices
==============

**Do:**

✅ Test with small datasets first
✅ Use descriptive output names
✅ Add detailed descriptions
✅ Check previous successful issues
✅ Be patient with large datasets

**Don't:**

❌ Process private data (not supported yet)
❌ Create duplicate issues
❌ Skip error messages
❌ Use special characters in names

FAQ
===

**Q: Do I need to install anything?**

A: No! Just create an issue. The forge runs on GitHub's servers.

**Q: How long do artifacts last?**

A: 90 days

**Q: Can I process private data?**

A: Currently only publicly accessible URLs are supported.

**Q: What if it fails?**

A: The bot will comment with error details. Check logs and try again.

**Q: Can I batch process?**

A: Yes! Create multiple issues, they'll run in parallel.

Architecture
============

For technical details about how the forge works, see :doc:`FORGE_ARCHITECTURE`.

For CI/CD server configuration, see :doc:`../server/index`.
