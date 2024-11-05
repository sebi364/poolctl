import toml
import os

config = toml.load(os.path.expanduser('~/.poolctl.toml'))

api_user = config.get('api_user')
api_url = config.get('api_url')
api_secret = config.get('api_secret')
api_verify = config.get('api_verify')
pve_peers = config.get('pve_peers')