# CiscoAutomationFramework

The CiscoAutomationFramework is a framework that is built on top of paramiko and pyserial that is designed to detect the type of Cisco device you connect to and issue commands based on the firmware its running and return consistent output. The goal is to give a network engineer an easy way to write automation scripts for Cisco devices.

## Project Goal

The goal of this project is to allow a Network Administrator to write scripts to gather data or modify configuration and be able to  run it against any Cisco device, regardless of hardware or firmware version and have the command sequence and syntax be correct while returning a consistent output.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Dependencies you need to have installed in your python environment.

```
paramiko 2.3.1
pyserial 3.4
```

### Installing copy to develop

Below are instructions for cloning a copy of the repository, building a virtual environment and setting your environment up to begin testing and developing.

Linux
```
git clone https://github.com/superadm1n/CiscoAutomationFramework.git
cd CiscoAutomationFramework
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

Windows

```
git clone https://github.com/superadm1n/CiscoAutomationFramework.git
cd CiscoAutomationFramework
virtualenv -p python3 env
env\scripts\activate
pip install -r requirements.txt
```


## Deployment

To leverage the framework for a project or to begin writing scripts using the framework these are the steps to install the framework in a virtual environment

Linux
```
mkdir myproject
cd myproject
virtualenv -p python3 env
source env/bin/activate
pip install git+https://github.com/superadm1n/CiscoAutomationFramework.git
```

Windows

```
mkdir myproject
cd myproject
virtualenv -p python3 env
env\scripts\activate
pip install git+https://github.com/superadm1n/CiscoAutomationFramework.git
```

Now you can begin creating your scripts using the framework, to import the framework below is an example of the import statements.

```
from CiscoAutomationFramework import connect_as_ssh
```

## Built With

* [Paramiko](http://www.paramiko.org/) - Used for SSH Engine
* [Pyserial](https://pythonhosted.org/pyserial/) - Used for Serial Engine


## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Kyle Kowalczyk** - *Initial work* - Github: [superadm1n](https://github.com/superadm1n) Personal Website: [SmallGuysIT](https://smallguysit.com)

## Code Documentation
[CiscoAutomationFramework Code Documentation](http://git.smallguysit.com/)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/superadm1n/CiscoAutomationFramework/blob/master/LICENSE) file for details

