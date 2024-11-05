import rich_click as click
import support.config as conf
from support import pveapi
from support.log import log
from support.pveapi import get, post
from support.misc import verify

@click.command(
    help = "Destroy a pool and all of it's ressources"
)
@click.option(
    "--name",
    "-n",
    default=None,
    help = "Name of the pool that should be destroyed"
)
def destroy(name):
    if name == None:
        log.error("You have to provide a pool-name!")
        exit(1)
    
    # check if pool with given name exists
    pools = get('pools').json()

    if name not in [p['poolid'] for p in pools['data']]:
        log.info(f"There's no pool named {name}, exiting...")
        exit()

    verify()