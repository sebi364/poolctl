from rich import traceback
traceback.install(show_locals=True)

import rich_click as click
from commands.snapshot import snapshot
from commands.rollback import rollback
from commands.status import status

@click.group()
def main():
    """PoolCTL is a handy python tool for managing pools in a proxmox based lab"""

main.add_command(snapshot)
main.add_command(rollback)
main.add_command(status)