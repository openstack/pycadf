# pyCADF documentation build configuration file
#
# This file is execfile()d with the current directory set to its containing dir.

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.apidoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'openstackdocstheme',
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
copyright = '2014-, OpenStack Foundation'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'default'
html_theme = 'openstackdocs'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {"nosidebar": "false"}

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (
        'index',
        'pyCADF.tex',
        'pyCADF Documentation',
        'OpenStack Foundation',
        'manual',
    ),
]

# -- Options for openstackdocstheme -------------------------------------------
openstackdocs_repo_name = 'openstack/pycadf'
openstackdocs_bug_project = 'pycadf'
openstackdocs_bug_tag = ''

# -- Options for sphinxcontrib.apidoc -----------------------------------------

apidoc_module_dir = '../../pycadf'
apidoc_output_dir = 'api'
apidoc_excluded_paths = ['tests']
