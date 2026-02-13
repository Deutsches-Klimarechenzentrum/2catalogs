.. Automated Generation

============================
Automated Generation
============================

The project includes a so called *"Forge system"* which allows users to trigger automatic
catalog generation through GitHub Issues and GitLab Continous Integration (CI/CD) integration.

Overview
--------

The Forge system allows users to request catalog generation through GitHub Issues without needing
to install or run tools locally. The system automatically:

* Validates user inputs
* Generates Intake v2 or STAC catalogs
* Creates downloadable artifacts
* Posts results back to the GitHub issue

Getting Started
---------------

Start with the :doc:`FORGE_QUICKSTART` guide for a quick introduction, or read the complete
:doc:`FORGE` documentation for detailed information.

.. toctree::
   :maxdepth: 4
   :caption: Forge Documentation
    user/index
    server/index