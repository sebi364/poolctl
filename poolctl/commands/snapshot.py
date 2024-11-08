import rich_click as click
from poolctl.support.log import log
from poolctl.support.pveapi import get, post
from poolctl.support.common import get_pool_resources


@click.command(help="Create a snapshot of all VMs in a pool")
@click.argument("pool")
@click.argument("snapshot")
@click.option(
    "--description",
    "-d",
    default="",
    help="Provide a description for the snapshot",
)
def snapshot(pool, snapshot, description):
    resources = get_pool_resources(pool)

    for r in resources:
        log.info(f"Creating snapshot of '{r}'")
        post(
            f"{r}/snapshot",
            data={"snapname": snapshot, "description": description, "vmstate": True},
        )
