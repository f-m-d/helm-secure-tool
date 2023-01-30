# Helm Secure Tool



An implementation of [**Stay at the Helm: secure Kubernetes deployments via graph generation and attack reconstruction**](https://ieeexplore.ieee.org/document/9860863) paper in Python



# Introduction

## Application scope
**Helm Secure Tool** is a tool to analyze the security of your Helm Charts and evaluate the security of you applications.

The main steps the tool works are:
* Starting from your Helm Chart folder, uses the **helm template** command to create a topological graph from the template elaboration
* _WORK IN PROGRESS:_  Evaluate the single nodes of the graph and the links with a security score
* _WORK IN PROGRESS:_  Show the riskiest path an attacker can take!

# Requirements
List of requirements to launch the tool:
* **Helm v3** at least (actual implementation does not use v2 Helm)
* **Python 3.x** al least


# Usage
To use the tool, launch it from command line>
_./main_yamlparser.py [PATH/TO/HELM/CHART/ ]  [NAMESPACE]_

Example:
_./main_yamlparser.py  "C:\User\Mike\Desktop\graphana-1.1.1\""test-namespace"_
