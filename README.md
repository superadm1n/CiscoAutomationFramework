[![Documentation Status](https://readthedocs.org/projects/ciscoautomationframework/badge/?version=latest)](https://ciscoautomationframework.readthedocs.io/en/latest/?badge=latest)

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/superadm1n/CiscoAutomationFramework)

# CiscoAutomationFramework

The CiscoAutomationFramework is a framework that is built on top of paramiko and pyserial that is designed to detect the type of Cisco device you connect to and issue commands based on the firmware its running and return consistent output. The goal is to give a network engineer an easy way to write automation scripts for Cisco devices.

## Project Goal

The goal of this project is to allow a Network Administrator to write scripts to gather data or modify configuration and be able to  run it against any Cisco device, regardless of hardware or firmware version and have the command sequence and syntax be correct while returning a consistent output.

## Currently supported Cisco operating systems

- IOS
- IOSXE
- NXOS

Previously I did attempt to support Cisco ASA's but found that more often than not to get the same
information for the parser methods I needed to hack together several commands to get the data
I needed and some methods I was unable to get the data I needed. The ASA's are something that I
would be open to supporting in the future if myself or someone is able to get them up to the same
level of support as IOS, IOSXE, and NXOS but is not on the roadmap currently.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Dependencies you need to have installed in your python environment.

```
paramiko 2.3.1
pyserial 3.4
```



## Deployment

To leverage the framework for a project or to begin writing scripts using the framework these are the steps to install the framework in a virtual environment

```
pip install CiscoAutomationFramework
```

Now you can begin creating your scripts using the framework, to import the framework below is an example of the import statements.

```
from CiscoAutomationFramework import connect_as_ssh
```

## Install latest version of the framework
Note installing directly from the master branch or a version branch from github is not the ideal solution for a 
production environment as it has the potential to have bugs that have less of a chance making it to the package
release on pypi.

That being said if you wish to have the latest features and are willing to live with a potential 
 for added bugs or help develop the framework, installing from github is where you should do and below
 is the command to install the package directly from github
```bash
pip install git+https://github.com/Superadm1n/CiscoAutomationFramework.git
```
or to install a specific branch
```bash
pip install git+https://github.com/Superadm1n/CiscoAutomationFramework.git@v1.0.8
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

## Built With

* [Paramiko](http://www.paramiko.org/) - Used for SSH Engine
* [Pyserial](https://pythonhosted.org/pyserial/) - Used for Serial Engine


## Versioning

NOTE! Until version 1.0 I will be committing directly to the master branch for all commits. 
After version 1.0 each new version will have its own version branch and wil be merged into master
once it is deemed stable.

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Kyle Kowalczyk** - *Initial work* - Github: [superadm1n](https://github.com/superadm1n) Personal Website: [KyleTK.com](https://kyletk.com)

## Code Documentation
[CiscoAutomationFramework Code Documentation](https://ciscoautomationframework.readthedocs.io/en/latest/)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/superadm1n/CiscoAutomationFramework/blob/master/LICENSE) file for details

