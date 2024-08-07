[![pdm-managed](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fpdm-project%2F.github%2Fbadge.json)](https://pdm-project.org)
![Static Badge](https://img.shields.io/badge/jsonargparse-d?link=https%3A%2F%2Fgithub.com%2Fomni-us%2Fjsonargparse)


# Easy AzureML (Beta)

This project attempts to reduce the boilerplate code when launching simple azureml jobs from command line.

It aims to:

- Be object oriented to enable end users to extend the SDK for their custom workflows, trying to reuse AzureML SDK V2 native classes as much as possible
- Be config driven (thanks to [jsonargparse](https%3A%2F%2Fgithub.com%2Fomni-us%2Fjsonargparse)) to improve reusability of objects and code
- Be, as it name states, easy to use (hence focused in simple usecases)
- Unify through wrappers the different flows and runs in Azure through a common interface

# Installation

Simply run 
```bash
pip install ezazml
```
# Quickstart
The main entrypoint is the CLI command. The following command will show you the help
```
ez-azml -h
```

You can run an example with
## Command
```
ez-azml --config configs/pytorch/main.yaml run
```
## Pipeline
```
ez-azml --config configs/pipeline/main.yaml run
```