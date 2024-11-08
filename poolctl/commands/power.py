import rich_click as click
from poolctl.support.log import log
from poolctl.support.pveapi import get, post
from poolctl.support.common import get_pool_resources


@click.command(help="Start all resources in a pool")
@click.argument("pool")
def start(pool):
    resources = get_pool_resources(pool)
    for r in resources:
        log.info(f"Starting '{r}'")
        post(f"{r}/status/start")


@click.command(help="Shutdown all resources in a pool")
@click.argument("pool")
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="Force stop VMs, if they don't shutdown after a given timeout",
)
@click.option("--timeout", "-t", default=120, help="Shutdown timeout (default = 120)")
def stop(pool, force, timeout):
    resources = get_pool_resources(pool)
    for r in resources:
        log.info(f"Shutting down '{r}'")
        post(f"{r}/status/shutdown", data={"forceStop": force, "timeout": timeout})


@click.command(help="Suspend all resources in a pool")
@click.argument("pool")
def suspend(pool):
    resources = get_pool_resources(pool)
    for r in resources:
        log.info(f"Suspending '{r}'")
        post(f"{r}/status/suspend")


@click.command(help="Resume all resources in a pool")
@click.argument("pool")
def resume(pool):
    resources = get_pool_resources(pool)
    for r in resources:
        log.info(f"Resuming '{r}'")
        post(f"{r}/status/resume")
