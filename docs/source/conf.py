# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))  # src code dir relative to this file

# -- Project information
project = "Easy AzureML"
copyright = "2024, Alejandro barón"  # noqa A001
author = "Alejandro Barón"

release = "0.1"
try:
    from ez_azml.__version__ import __version__

    version = __version__
except ImportError:
    version = "0.1.0"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",  # Core library for html generation from docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables
    "sphinx.ext.napoleon",
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
