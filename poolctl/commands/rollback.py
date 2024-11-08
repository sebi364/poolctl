import rich_click as click
from poolctl.support.log import log
from poolctl.support.pveapi import get, post
from poolctl.support.common import get_pool_resources


@click.command(help="Rollback to a previous snapshot of a pool")
@click.argument("pool")
@click.argument("snapshot")
def rollback(pool, snapshot):
    resources = get_pool_resources(pool)

    for r in resources:
        snapshots = [s["name"] for s in get(f"{r}/snapshot").json()["data"]]
        if snapshot in snapshots:
            log.info(f"Rolling back snapshot off '{r}' to '{snapshot}'")
            post(f"{r}/snapshot/{snapshot}/rollback")
        else:
            log.error(f"The target {r} has no snapshot named {snapshot}. Skipping...")
            log.info(
                f"This target can be rolled back to one of the following snapshots: {snapshots}"
            )
