import rich_click as click
from poolctl.support.log import log, console
from poolctl.support.pveapi import get, post
from rich.table import Table, box


def paint_status(status):
    if status == "running":
        return f"[bold green]{status}[/]"
    elif status == "stopped":
        return f"[bold red]{status}[/]"
    else:
        return f"[bold yellow]{status}[/]"


def pool_overview():
    data = get("cluster/resources").json()["data"]
    pools = {}

    for p in data:
        if p["type"] == "pool":
            pools[p["pool"]] = {
                "clients": 0,
                "cpu_aloc": 0,
                "cpu_used": 0,
                "mem_aloc": 0,
                "mem_used": 0,
                "hdd_aloc": 0,
            }

    pools["[italic](other)"] = {
        "clients": 0,
        "cpu_aloc": 0,
        "cpu_used": 0,
        "mem_aloc": 0,
        "mem_used": 0,
        "hdd_aloc": 0,
    }

    for r in data:
        if r["type"] == "qemu" or r["type"] == "lxc":
            if "pool" not in r.keys():
                r["pool"] = (
                    "[italic](other)"  # set empty pool, if not assigned to a pool
                )

            pools[r["pool"]]["clients"] += 1
            pools[r["pool"]]["cpu_aloc"] += (
                r["maxcpu"] if bool(r["template"]) == False else 0
            )
            pools[r["pool"]]["cpu_used"] += r["cpu"]
            pools[r["pool"]]["mem_aloc"] += (
                r["maxmem"] if bool(r["template"]) == False else 0
            )
            pools[r["pool"]]["mem_used"] += r["mem"]
            pools[r["pool"]]["hdd_aloc"] += r["maxdisk"]

    # format back to list
    output = []
    for i in pools.keys():
        pools[i]["pool"] = i
        output.append(pools[i])

    # -----------------------------------------------------------------

    table = Table(box=box.MINIMAL, highlight=True, show_footer=True)

    table.add_column("Poolname:")
    table.add_column("Clients:", footer=f"{sum([i['clients'] for i in output])}")
    table.add_column(
        "Memory (aloc.):",
        footer=f"{round(sum([i['mem_aloc'] for i in output]) / 2**30, 2)} GB",
    )
    table.add_column(
        "Memory (used):",
        footer=f"{round(sum([i['mem_used'] for i in output]) / 2**30, 2)} GB",
    )
    table.add_column(
        "Core (aloc.):", footer=f"{round(sum([i['cpu_aloc'] for i in output]), 2)} CPU"
    )
    table.add_column(
        "Core (used):", footer=f"{round(sum([i['cpu_used'] for i in output]), 2)} CPU"
    )
    table.add_column(
        "Storage:",
        footer=f"{round(sum([i['hdd_aloc'] for i in output]) / 2**30, 2)} GB",
    )

    for p in output:
        table.add_row(
            f"[bold]{p['pool']}[/]",
            f"{p['clients']}",
            f"{round(p['mem_aloc'] / 2**30, 2)} GB",
            f"{round(p['mem_used'] / 2**30, 2)} GB",
            f"{p['cpu_aloc']} CPU",
            f"{round(p['cpu_used'], 2)} CPU",
            f"{round(p['hdd_aloc'] / 2**30, 2)} GB",
        )

    console.print(table)


def pool_detail(pool):
    output = []
    for m in get(f"pools/{pool}").json()["data"]["members"]:
        output.append(
            [
                m["status"],
                m["name"],
                m["vmid"],
                m["type"],
                m["maxmem"] if bool(m["template"]) == False else 0,
                m["mem"],
                m["maxcpu"] if bool(m["template"]) == False else 0,
                m["cpu"],
                m["maxdisk"],
                bool(m["template"]),
            ]
        )

    table = Table(box=box.MINIMAL, highlight=True, show_footer=True)
    table.add_column("Status:")
    table.add_column("Name:")
    table.add_column("Vmid:")
    table.add_column("Type:")
    table.add_column(
        "Memory (aloc.):", footer=f"{round(sum([i[4] for i in output]) / 2**30, 2)} GB"
    )
    table.add_column(
        "Memory (used):", footer=f"{round(sum([i[5] for i in output]) / 2**30, 2)} GB"
    )
    table.add_column(
        "Core (aloc.):", footer=f"{round(sum([i[6] for i in output]), 2)} CPU"
    )
    table.add_column(
        "Core (used):", footer=f"{round(sum([i[7] for i in output]), 2)} CPU"
    )
    table.add_column(
        "Storage:", footer=f"{round(sum([i[8] for i in output]) / 2**30, 2)} GB"
    )
    table.add_column("Template:")

    for r in output:
        table.add_row(
            f"{paint_status(r[0])}",
            f"[bold]{r[1]}[/]",
            f"{r[2]}",
            f"{r[3]}",
            f"{round(r[4] / 2**30, 2)} GB",
            f"{round(r[5] / 2**30, 2)} GB",
            f"{r[6]} CPU",
            f"{round(r[7], 2)} CPU",
            f"{round(r[8] / 2**30, 2)} GB",
            f"{r[9]}",
        )

    console.print(table)


@click.command(help="Show misc. stats")
@click.option(
    "--pool", "-p", default=None, help="Name of the pool you want to know more about"
)
def status(pool):
    if pool:
        pools = get("pools").json()["data"]
        if pool not in [p["poolid"] for p in pools]:
            log.info(f"There's no pool named {pool}, exiting...")
            exit()
        pool_detail(pool)
    else:
        pool_overview()
