import rich_click as click
import poolctl.support.pveapi


@click.command(help="Configure poolctl")
def configure():
    conf.configure()
