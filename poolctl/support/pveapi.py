from poolctl.support.log import log
from pathlib import Path
import subprocess
import requests
import toml
import os

# ------------------------------------------------------------------------------------

cookies = {}
headers = {}


class LiveConf:
    def __init__(self):
        # get cookie
        process = subprocess.Popen(
            ["perl", f"{Path(__file__).resolve().parent.parent}/scripts/get_token.pl"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = process.communicate()
        cookie, csrftoken = output.decode("utf-8").split(";")
        # config
        self.api_url = f"https://127.0.0.1:8006/api2/json/"
        self.api_verify = False
        self.headers = {"CSRFPreventionToken": csrftoken.strip()}
        self.cookies = {"PVEAuthCookie": cookie.strip()}
        # hide ssl warnings
        requests.packages.urllib3.disable_warnings()


class FileConf:
    def __init__(self):
        config_dir = (
            Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
            / "poolctl"
        )
        config_file = config_dir / "poolctl.toml"

        if not config_file.exists():
            log.critical("Unable to read config file!")
            log.info("You can initialize poolctl using 'poolctl configure'")

            self.config_type = "toml"
            self.api_url = ""
            self.api_verify = True
            self.headers = {}
            self.cookies = {}
        else:
            config = toml.load(config_file)
            self.config_type = "toml"
            self.api_url = config.get("api_url")
            self.api_verify = config.get("api_verify")
            self.headers = {
                "Authorization": f"PVEAPIToken={config.get('api_user')}={config.get('api_secret')}"
            }
            self.cookies = {}

            if self.api_verify == False:
                requests.packages.urllib3.disable_warnings()


# check if the script is running as the root user on a PVE host
try:
    if os.path.exists("/usr/bin/pvesh") and os.geteuid() == 0:
        conf = LiveConf()
    else:
        conf = FileConf()

except:
    # probably not a pve host, use normal config
    conf = FileConf()

# ------------------------------------------------------------------------------------


def get(endpoint):
    r = requests.get(
        f"{conf.api_url}{endpoint}",
        headers=conf.headers,
        cookies=conf.cookies,
        verify=conf.api_verify,
    )
    return r


def post(endpoint, data=None):
    r = requests.post(
        f"{conf.api_url}{endpoint}",
        headers=conf.headers,
        cookies=conf.cookies,
        verify=conf.api_verify,
        json=data,
    )
    return r
