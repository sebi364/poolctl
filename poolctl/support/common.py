from support.pveapi import get, post
from support.log import log

def get_pool_resources(pool):
    if pool == None:
        log.error("You have to provide a pool-name!")
        exit(1)
    
    # check if pool with given name exists
    pools = get('pools').json()

    if pool not in [p['poolid'] for p in pools['data']]:
        log.info(f"There's no pool named {pool}, exiting...")
        exit()
    
    # get resources
    resources = []
    r = get(f'pools/{pool}').json()
    for m in r['data']['members']:
        resources.append(f"nodes/{m['node']}/{m['id']}")
    
    if len(resources) == 0:
        log.info("The pool is empty, there's nothing to do!")
        exit(0)
    
    return resources