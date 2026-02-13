# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '2catalogs'
copyright = '2026, Fabian Wachsmann'
author = 'Fabian Wachsmann'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'myst_parser',  # For Markdown support
]

# Markdown files support
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'  # Modern, clean theme
html_static_path = ['_static']
html_title = '2catalogs Documentation'

# Theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "show_toc_level": 2,
    "repository_url": "https://github.com/Deutsches-Klimarechenzentrum/2catalogs/",
    "use_repository_button": True,
    "extra_footer": '''
        <div style="text-align: center;">
            <a href="https://www.dkrz.de/en/about-en/contact/impressum" target="_blank">Imprint</a> and
            <a href="https://www.dkrz.de/en/about-en/contact/en-datenschutzhinweise" target="_blank">Privacy Policy</a>
        </div>
    ''',
}

html_logo = '_static/dkrz_logo.png'

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google and NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# InterSphinx mapping for linking to other projects
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'xarray': ('https://docs.xarray.dev/en/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}

# MyST Parser settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
]
