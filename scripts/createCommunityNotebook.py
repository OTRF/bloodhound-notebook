#!/usr/bin/env python3

# Project: BloodHound Notebook
# Author: Roberto Rodriguez (@Cyb3rWard0g)
# License: GPLv3
# Reference:

import yaml
import copy
from jinja2 import Template
import glob
from os import path
import nbformat as nbf

# ***** Processing Community Cypher Queries *****
print("[+] Processing files inside {} directory".format('../queries'))
print("[+] Opening community cypher queries yaml files..")
yaml_files = glob.glob(path.join(path.dirname(__file__), '../queries', "*.yml"))
yaml_loaded = [yaml.safe_load(open(yf).read()) for yf in yaml_files]

# ******** Creating BloodHound Cypher Community Notebook ********
print("\n[+] Creating the BloodHound Cypher Queries Community Notebook..")
# **** METADATA ****
metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.7.3"
    }
}
# **** INITIALIZE NOTEBOOK ****
nb = nbf.v4.new_notebook(metadata=metadata)
nb['cells'] = []
# *** TITLE ****
nb['cells'].append(nbf.v4.new_markdown_cell("# Queries Notebook"))

# *** METADATA ****
nb['cells'].append(nbf.v4.new_markdown_cell(
    """
* **Author**: Roberto Rodriguez (@Cyb3rWard0g)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
    """
))

# **** SETUP ****
# **** IMPORT LIBRARIES ****
nb['cells'].append(nbf.v4.new_markdown_cell("## Import Libraries"))
nb['cells'].append(nbf.v4.new_code_cell("from py2neo import Graph"))

# **** INITIALIZE GRAPH SESSION ****
nb['cells'].append(nbf.v4.new_markdown_cell("## Initialize Graph Variable"))
nb['cells'].append(nbf.v4.new_code_cell("graph = Graph(password='wardog')"
))

# **** COMMUNITY CYPHER QUERIES ****
nb['cells'].append(nbf.v4.new_markdown_cell("## Community Cypher Queries"))
for yaml in yaml_loaded:
    print("  [>] Processing query {}..".format(yaml['title']))
    # **** METADATA ****
    nb['cells'].append(nbf.v4.new_markdown_cell("""## {}
**Author:** {}
\n**Description:** {}
""".format(yaml['title'],yaml['author'],yaml['description'])))
    # **** CYPHER QUERY ****
    nb['cells'].append(nbf.v4.new_code_cell("""graph.run(
'''
{}
'''
).data()""".format(yaml['query'])))

# **** Writing Bloodhound Cypher Community Notebook *****
print("\n  [>] Writing notebook to ../docs/notebooks/cypher/queries_notebook.ipynb")
nbf.write(nb, "../docs/notebooks/cypher/queries_notebook.ipynb")

# ***** Creating Query Summary Table *****
table_template = Template(open('templates/table_template.md').read())
print("\n[+] Creating Community Cypher Summary Table.")
yaml_for_render = copy.deepcopy(yaml_loaded)
markdown = table_template.render(community=yaml_for_render)
open('../docs/notebooks/cypher/queries_table.md', 'w').write(markdown)