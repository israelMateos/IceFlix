# IceFlix: Main service

Made by **Israel Mateos Aparicio Ruiz Santa Quiteria** for Distributed Systems course.

The main objective of this proyect is developing a **distributed system** based on **microservicies**, taking Netflix as a reference. The microservice **Main** acts as a gateway to the system for clients. These may get references to _Authenticator_, _MediaCatalog_ and _FileService_ services through its interface. Altogether, these microservices form an application which offers files on demand.


## How to use

**Prerequisites**: `Python 3.10` or greater, `pip`.

Before running the service, it is necessary to install the package via the command-line, using the following command while on the root directory of this repository:

```console
$ pip install .
```

After installing it, you can run the service by the `run_service` script, using the following command while on the root directory of this repository:

```console
$ ./run_service
```

Please, ensure that the script has execute permissions for the user who is running it.

## Project structure

This repository contains the following files and directories:

- `configs` has the configuration file for the service.
- `iceflix` is the main Python package.
- `iceflix/__init__.py` is an file needed by Python to recognise the `iceflix` directory as a Python module, and where the `IceFlix` package importation is defined.
- `iceflix/cli.py` contains several functions to handle the basic console entry points
  defined in `python.cfg`.
- `iceflix/iceflix.ice` contains the Slice interface definition for the lab.
- `iceflix/main.py` has the implementation of Main service, along with the service servant itself.
- `pyproject.toml` defines the build system used in the project.
- `run_service` is a script that can be run directly from the repository root directory. It is able to run the Main service.
- `setup.cfg` is a Python distribution configuration file for Setuptools.