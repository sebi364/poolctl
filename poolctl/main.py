import poolctl.support.config

from rich import traceback
traceback.install(show_locals=True)

import rich_click as click

from poolctl.commands.configure import configure
from poolctl.commands.snapshot import snapshot
from poolctl.commands.rollback import rollback
from poolctl.commands.status import status
from poolctl.commands.power import start
from poolctl.commands.power import suspend
from poolctl.commands.power import resume
from poolctl.commands.power import stop

@click.group()
def main():
    """PoolCTL is a handy python tool for managing pools in a proxmox based lab"""

main.add_command(configure)
main.add_command(snapshot)
main.add_command(rollback)
main.add_command(status)
main.add_command(start)
main.add_command(suspend)
main.add_command(resume)
main.add_command(stop)