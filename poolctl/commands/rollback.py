import rich_click as click
from poolctl.support.log import log
from poolctl.support.pveapi import get, post
from poolctl.support.common import get_pool_resources

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
    
    # check if pool with given name exists
    resources = get_pool_resources(pool)

    # roll back snapshot
    for r in resources:
        snapshots = [s['name'] for s in get(f"{r}/snapshot").json()['data']]
        if name in snapshots:
            log.info(f"Rolling back snapshot off '{r}' to '{name}'")
            post(f"{r}/snapshot/{name}/rollback")
        else:
            log.error(f"The target {r} has no snapshot named {name}. Skipping...")
            log.info(f"This target can be rolled back to one of the following snapshots: {snapshots}")