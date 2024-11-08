import string
import random
from poolctl.support.log import log, console

def randstring(length):
    return ''.join([random.choice(string.ascii_lowercase) for i in range(length)])

def verify():
    password = randstring(8)
    userinput = console.input(f"Please enter the following password to verify this action: '{password}':")
    if password != userinput:
        log.error("Wrong password, exiting...")
        exit()