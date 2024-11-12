import rich_click as click
import poolctl.support.pveapi
from poolctl.support.log import log
import toml
import os
from pathlib import Path
import questionary
import re
import requests

CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
CONFIG_DIR = CONFIG_HOME / "poolctl"
CONFIG_FILE = CONFIG_DIR / "poolctl.toml"

def match_api(hostname):
    return bool(re.match(r"^https://.+/api2/json/$", hostname))

def match_user(user):
    return bool(re.match(r"^.+@.+\!.+$", user))

@click.command(help="Configure poolctl")
def configure():
    config = {}

    config["api_user"] = questionary.text("What API-user should poolctl use? [Example: root@pam!poolctl]", validate = match_user).ask()
    config["api_url"] = questionary.text("What API-endpoint should poolctl use? [Example: https://pvehost.lan:8006/api2/json/]", validate = match_api).ask()
    config["api_secret"] = questionary.password("What API-secret should poolctl use?").ask()
    config["api_verify"] = questionary.confirm("Do you have a valid SSL certificate?").ask()

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(
            config["api_url"],
            verify = config["api_verify"],
            headers = {
                "Authorization": f"PVEAPIToken={config['api_user']}={config['api_secret']}"
            }
        )
    except Exception as e:
        log.error("There was an error while connecting to the server!")
        log.error(e)
        exit(1)
    
    if r.status_code != 200:
        log.error(f"Connection was successfull, but the authentication failed: {r.status_code}")
        log.error(r.text)
        exit(1)
    else:
        log.info("Config is valid! Writing to file...")

    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    with open(CONFIG_FILE, "w") as f:
        toml.dump(config, f)