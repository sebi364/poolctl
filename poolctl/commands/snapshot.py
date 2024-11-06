import rich_click as click
from support.log import log
from support.pveapi import get, post

@click.command(
    help = "Create a snapshot of all VMs in a pool"
)
@click.option(
    "--pool",
    "-p",
    default=None,
    help = "Name of the pool you want to create a shanpshot off"
)
@click.option(
    "--name",
    "-n",
    default=None,
    help = "Name of the snapshot"
)
@click.option(
    "--description",
    "-d",
    default='',
    help = "Provide a description for the snapshot",
)
def snapshot(pool, name, description):
    if name == None:
        log.error("You have to provide a snapshot-name!")
        exit(1)
    if pool == None:
        log.error("You have to provide a pool-name!")
        exit(1)
    
    # check if pool with given name exists
    pools = get('pools').json()

    if pool not in [p['poolid'] for p in pools['data']]:
        log.info(f"There's no pool named {pool}, exiting...")
        exit()
    
    # get targets
    targets = []
    r = get(f'pools/{pool}').json()
    for m in r['data']['members']:
        targets.append(f"nodes/{m['node']}/{m['id']}")
    
    if len(targets) == 0:
        log.info("The pool is empty, there's nothing to do!")
        exit(0)

    # snapshot
    for t in targets:
        log.info(f"Creating snapshot off '{t}'")
        post(
            f"{t}/snapshot",
            data={
                'snapname': name,
                'description': description,
                'vmstate': True
            }
        )