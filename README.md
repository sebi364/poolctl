# Poolctl
Poolctl is a python CLI tool to simplify managing proxmox resources on a pool basis.

## Background
Proxmox resource pools are a great way of keepig multiple projects / lab-environments organized, however I felt like it was missing the ability to perform actions on all VMs in a specific Pool.

**For example:** I have an Active-Directory lab for school with +/- 8 VMs that are all in one pool named "lab1". I want to test something, but I'm pretty sure that this will probably break something and fixnig it will be quite a mess. Making Snapshots of all VMs and rolling them back by hand can be quit a burden, that's why I made this tool.

## Features
Poolctl provides a few commands that can help you manage a lab:
```bash
# create a new snapshot of all resource in a pool
poolctl snapshot -p <poolname> -n <snapshotname>

# rollback all resources to a snapshot
poolctl rollback -p <poolname> -n <snapshotname>

# show a handy status page
poolctl status
poolctl status -p <poolname>

# power controlls
poolctl start -p <poolname>
poolctl stop -p <poolname>
poolctl suspend -p <poolname>
poolctl resume -p <poolname>
```

## Installation
(ToDo)