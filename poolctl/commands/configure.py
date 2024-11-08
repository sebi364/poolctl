import rich_click as click
from poolctl.support.config import conf

@click.command(
    help = "Configure poolctl"
)
def configure():
    conf.configure()