> [!WARNING]
> This whole project is still very much a work in progress, use at your own risk.

# Poolctl
Poolctl is a python CLI tool to simplify managing proxmox resources on a pool basis.

## Background
Proxmox resource pools are a great way of keepig multiple projects / lab-environments organized. However I felt that they lacked functionality to perform actions on all VMs in a specific Pool.

**For example:** I have an Active Directory lab for school with around 8 VMs, all grouped into a pool named "lab1". I want to test something, but I'm fairly certain it will break something, and fixing it would be a hassle. Creating snapshots of all VMs and rolling them back manually can be cumbersome, that's why I created this tool.

## Features
Poolctl offers several commands to help you manage your lab environments more easily:
```bash
# create a new snapshot of all resource in a pool
poolctl snapshot <poolname> <snapshotname>

# rollback all resources to a snapshot
poolctl rollback <poolname> <snapshotname>

# show a handy status page
poolctl status
poolctl status -p <poolname>

# power controlls
poolctl start <poolname>
poolctl stop <poolname>
poolctl suspend <poolname>
poolctl resume <poolname>
```

## Getting started
1. Install poolctl using [pipx](https://github.com/pypa/pipx):
    ```bash
    pipx install git+https://github.com/sebi364/poolctl.git
    ```
2. Create a new API key under `Datacenter > Permissions API Tokens > Add`. Keep in mind that you will need to give the key high enough privilidges *(or just make a key for the root user with no privilege separation)*
3. Run `poolctl configure`, this command will create the config file for you.
    ```
    root@pve:~# poolctl configure
    API-User: xxxx@pam!xxxx
    API-URL: https://xxxxxxx/api2/json/
    API-Secret: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    SSL [True/False]: True
    ```