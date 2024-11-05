import rich_click as click
import support.config as conf
from support import pveapi
from support.log import log
from support.pveapi import get, post

@click.command(
    help = "Create a new pool"
)
@click.option(
    "--name",
    "-n",
    default=None,
    help = "Name of the pool that should be created"
)
@click.option(
    "--comment",
    "-c",
    default='',
    help = "Provide a comment for the pool",
)
@click.option(
    "--force",
    "-f",
    default=False,
    help = "Force creation of a pool",
    is_flag=True
)
def create(name, comment, force):
    if name == None:
        log.error("You have to provide a pool-name!")
        exit(1)
    
    pools = get('pools').json()

    # check if pool with given name exists
    was_forced = False
    
    if name not in [p['poolid'] for p in pools['data']]:
        log.info(f"No pool named {name}, creating a new one.")
    else:
        log.warn(f"A pool with the given name ({name}) already exists, exiting...")
        if not force:
            log.info("You can use --force, to force this action")
            exit()
        else:
            log.warn("continuing anyway...")
            was_forced = True
        
    # create a new pool
    log.info("Creating creating new pool...")
    r = post(
        "pools",
        data = {
            'poolid': name,
            'comment': comment
        }
    )

    # create a new VXLan
    log.info("Creating a new VXLan...")
    r = post(
        "cluster/sdn/zones",
        data={
            'type': 'vxlan',
            'zone': name,
            'peers': conf.pve_peers
        }
    )