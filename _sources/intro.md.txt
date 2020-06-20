# BloodHound Notebook Project

[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

A community-driven effort to document and share cypher queries via Jupyter Notebooks.

## Use Cases:

* Teach about Neo4j Cypher applied to BloodHound via notebooks
* Capture Input (Cypher Queries) and Output(Results) for documentation/reports purposes
* Automate the execution of several queries in a practical and easy-to-reproduce way
* Allow the InfoSec community to run Cypher Queries interactively through a browser (Nothing installed locally) and for FREE

## How To Collaborate

* The InfoSec community benefits the more queries we share!
* Open a PR and share a query following a similar YAML file format:

```
title: Kerberoastable Users
id: A272812C-1FF8-4D4D-B24A-69F482CB1133
creation_date: 2020/06/20
author: Ryan Hausknecht (@haus3c)
description: Find All Users with an SPN/Find all Kerberoastable Users
references:
  - https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/
query: |-
  MATCH (n:User)WHERE n.hasspn=true
  RETURN n.name
```
* Save that query in the [queries](https://github.com/OTRF/bloodhound-notebook/tree/master/queries) folder.
* The following [script](https://github.com/OTRF/bloodhound-notebook/blob/master/scripts/createCommunityNotebook.py) then is run after the PR is approved to update all the docs and community notebook.

## Author

Roberto Rodriguez ([@Cyb3rWard0g](https://twitter.com/Cyb3rWard0g))
