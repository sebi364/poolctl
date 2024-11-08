import toml
import os
from pathlib import Path
from poolctl.support.log import log

CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
CONFIG_DIR = CONFIG_HOME / "poolctl"
CONFIG_FILE = CONFIG_DIR / "poolctl.toml"

class Conf():
    def __init__(self):
        if not CONFIG_FILE.exists():
            log.critical("Unable to read config file!")
            log.info("You can initialize poolctl using 'poolctl config'")

            self.api_user = ""
            self.api_url = ""
            self.api_secret = ""
            self.api_verify = ""
            return
        else:
            config = toml.load(CONFIG_FILE)
            self.api_user = config.get('api_user')
            self.api_url = config.get('api_url')
            self.api_secret = config.get('api_secret')
            self.api_verify = config.get('api_verify')
    
    def configure(self):
        config = {}

        config['api_user'] = input("API-User: ")
        config['api_url'] = input("API-URL: ")
        config['api_secret'] = input("API-Secret: ")
        config['api_verify'] = bool(input("SSL [True/False]: "))

        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir()

        with open(CONFIG_FILE, 'w') as f:
            toml.dump(config, f)

conf = Conf()