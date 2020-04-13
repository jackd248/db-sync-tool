# TYPO3 Database Sync

Simple python script to synchronize a TYPO3 database from a remote to your local system.

## Prerequisite

The script using python 2. Is it necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 
You can do this by the following command:

```bash
apt install -y python-pip
```

## Configuration

The `host.json` contains important information about the remote and the local system. 
You need to specify the SSH credentials for the remote system and the path to the `LocalConfiguration.php` of both systems.

```bash
# Copy/edit host.json
mv host.json.dist host.json
```

## Usage

```bash
# Run python script
python sync.py
```

You are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 