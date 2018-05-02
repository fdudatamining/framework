# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = "fdudatamining"
version = "0.1"
release = "0.0.1"
author = 'fdudatamining'
copyright = '2018, fdudatamining'

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['setup', 'tests']
pygments_style = 'sphinx'

html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'FDUDataminingFrameworkdoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'FDUDataminingFramework.tex', 'FDU Datamining Framework Documentation',
     'fdudatamining', 'manual'),
]

man_pages = [
    (master_doc, 'fdudataminingframework', 'FDU Datamining Framework Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'FDUDataminingFramework', 'FDU Datamining Framework Documentation',
     author, 'FDUDataminingFramework', 'One line description of project.',
     'Miscellaneous'),
]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
]

def run_apidoc(_):
    from sphinx.apidoc import main
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(cur_dir,"..","framework")
    output_path = os.path.join(cur_dir, "autogen")
    # NOTE: This doesn't seem to work, so I just use subprocess
    # main([None, '-e', '-f', '-o', output_path, module])
    from subprocess import check_call
    check_call(['sphinx-apidoc', '-e', '-f', '-o', output_path, module])

def setup(app):
    app.connect('builder-inited', run_apidoc)
