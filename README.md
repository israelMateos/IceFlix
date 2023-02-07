# IceFlix: Main service

https://github.com/israelMateos/IceFlix/

Made by **Israel Mateos Aparicio Ruiz Santa Quiteria** for Distributed Systems course.

The main objective of this project is developing a **distributed system** based on **microservicies**, taking Netflix as a reference. The microservice **Main** acts as a gateway to the system for clients. These may get references to _Authenticator_, _MediaCatalog_ and _FileService_ services through its interface. Altogether, these microservices form an application which offers files on demand.


## How to use

**Prerequisites**: `Python 3.10` or greater, `pip`, `IceBox`, `IceStorm` (the packages corresponding to these last 2 change depending on your Linux distribution).

Before running the service, it is necessary to install the package via the command-line, using the following command while on the root directory of this repository:

```console
$ pip install .
```

After installing it, you can either create an IceStorm instance and connect to it, or connect to an existing IceStorm instance.

**1. Create your own IceStorm instance.**

You can create your own IceStorm instance by using the following command while on the root directory of this repository:

```console
$ ./run_icestorm
```

Please, ensure that the script has execute permissions for the user who is running it. No more configurations are required, since the application is already configured to connect to this instance by default in `main.config`.

**2. Connect to an existing IceStorm instance.**

In order to connect to an existing IceStorm instance, you must ask for its proxy first. Once you have it, you have to modify the value of the property `IceStorm.TopicManager` in `main.config` in the following way: `IceStorm.TopicManager={proxy for the instance}` (do not write the brackets).

***

After creating your IceStorm instance or modifying the configuration with the expected instance, you can run the service by the `run_service` script, using the following command while on the root directory of this repository:

```console
$ ./run_service
```

Please, ensure that the script has execute permissions for the user who is running it.

## Project structure

This repository contains the following files and directories:

- `configs` has the configuration file for the service, as well as for the IceStorm service.
- `iceflix` is the main Python package.
- `iceflix/__init__.py` is an file needed by Python to recognise the `iceflix` directory as a Python module, and where the `IceFlix` package importation is defined.
- `iceflix/cli.py` contains several functions to handle the basic console entry points
  defined in `python.cfg`.
- `iceflix/iceflix.ice` contains the Slice interface definition for the lab.
- `iceflix/main.py` has the implementation of Main service, along with the service servant itself.
- `pyproject.toml` defines the build system used in the project.
- `run_service` is a script that can be run directly from the repository root directory. It is able to run the Main service.
- `run_icestorm` is a script that can be run directly from the repository root directory. It is able to create an instance of the IceStorm service.
- `setup.cfg` is a Python distribution configuration file for Setuptools.
