import rich_click as click
from support.log import log
from support.pveapi import get, post

@click.command(
    help = "Rollback to a snapshot of a pool"
)
@click.option(
    "--pool",
    "-p",
    default=None,
    help = "Name of the pool you want to rollback"
)
@click.option(
    "--name",
    "-n",
    default=None,
    help = "Name of the snapshot"
)
def rollback(pool, name):
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

    # roll back snapshot
    for t in targets:
        snapshots = [s['name'] for s in get(f"{t}/snapshot").json()['data']]
        if name in snapshots:
            log.info(f"Rolling back snapshot off '{t}' to '{name}'")
            post(f"{t}/snapshot/{name}/rollback")
        else:
            log.error(f"The target {t} has no snapshot named {name}. Skipping...")
            log.info(f"This target can be rolled back to one of the following snapshots: {snapshots}")