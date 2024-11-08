import rich_click as click
from poolctl.support.log import log
from poolctl.support.pveapi import get, post
from poolctl.support.common import get_pool_resources


@click.command(help="Create a snapshot of all VMs in a pool")
@click.option(
    "--pool",
    "-p",
    default=None,
    help="Name of the pool you want to create a shanpshot off",
)
@click.option("--name", "-n", default=None, help="Name of the snapshot")
@click.option(
    "--description",
    "-d",
    default="",
    help="Provide a description for the snapshot",
)
def snapshot(pool, name, description):
    if name == None:
        log.error("You have to provide a snapshot-name!")
        exit(1)

    resources = get_pool_resources(pool)

    # snapshot
    for r in resources:
        log.info(f"Creating snapshot of '{r}'")
        post(
            f"{r}/snapshot",
            data={"snapname": name, "description": description, "vmstate": True},
        )
