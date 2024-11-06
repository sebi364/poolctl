import rich_click as click
from support.log import log, console
from support.pveapi import get, post
from rich.table import Table, box

def pool_overview():
    output = []

    for p in get('pools').json()['data']:
        d = get(f"pools/{p['poolid']}").json()['data']

        vms = 0
        cpu_aloc = 0
        cpu_used = 0
        mem_aloc = 0
        mem_used = 0
        hdd_aloc = 0

        for m in d['members']:
            vms += 1
            cpu_aloc += m['maxcpu']
            cpu_used += m['cpu']
            mem_aloc += m['maxmem']
            mem_used += m['mem']
            hdd_aloc += m['maxdisk']
        
        output.append([
            p['poolid'],
            vms,
            mem_aloc,
            mem_used,
            cpu_aloc,
            cpu_used,
            hdd_aloc
        ])

    # -----------------------------------------------------------------

    table = Table(box=box.MINIMAL, highlight=True, show_footer=True)

    table.add_column("Poolname:")
    table.add_column("Clients:", footer=f"{sum([i[1] for i in output])}")
    table.add_column("Memory (aloc.):", footer=f"{round(sum([i[2] for i in output]) / 2**30, 2)} GB")
    table.add_column("Memory (used):", footer=f"{round(sum([i[3] for i in output]) / 2**30, 2)} GB")
    table.add_column("Core (aloc.):", footer=f"{round(sum([i[4] for i in output]), 2)} CPU")
    table.add_column("Core (used):", footer=f"{round(sum([i[5] for i in output]), 2)} CPU")
    table.add_column("Storage:", footer=f"{round(sum([i[6] for i in output]) / 2**30, 2)} GB")

    for p in output:
        table.add_row(
            f"[bold]{p[0]}[/]",
            f"{p[1]}",
            f"{round(p[2] / 2**30, 2)} GB",
            f"{round(p[3] / 2**30, 2)} GB",
            f"{p[4]} CPU",
            f"{round(p[5], 2)} CPU",
            f"{round(p[6] / 2**30, 2)} GB"
        )
        
    console.print(table)

def pool_detail(pool):
    console.print(get(f'pools/{pool}').json())

@click.command(
    help = "Show misc. stats"
)
@click.option(
    "--pool",
    "-p",
    default=None,
    help = "Name of the pool you want to know more about"
)
def status(pool):
    if pool:
        pools = get('pools').json()['data']
        if pool not in [p['poolid'] for p in pools]:
            log.info(f"There's no pool named {pool}, exiting...")
            exit()
        pool_detail(pool)
    else:
        pool_overview()