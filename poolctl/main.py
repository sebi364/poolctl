from rich import traceback
traceback.install(show_locals=True)

import rich_click as click

from commands.create import create
from commands.destroy import destroy
from commands.snapshot import snapshot
from commands.rollback import rollback

@click.group()
def main():
    """PoolCTL is a handy python script for managing pools in a proxmox based lab"""

main.add_command(create)
main.add_command(destroy)
main.add_command(snapshot)
main.add_command(rollback)