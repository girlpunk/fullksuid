import math
import os
import re
import secrets
import struct
import threading
from datetime import datetime

import netifaces

from fullksuid import validation
from fullksuid.Id import Id
from fullksuid.Instance import Instance
from fullksuid.Schemes import Schemes

# this = sys.modules[__name__]

environment = ""
lastTimestamp = 0
currentSequence = 0
lock = threading.Lock()

all_zeroes = re.compile(r"^0+$")


def get_environment() -> str:
    global environment
    return environment


def set_environment(value: str):
    validation.check_prefix('environment', value)
    global environment
    environment = value


def generate(resource: str) -> Id:
    global environment
    global lastTimestamp
    global currentSequence
    global lock
    global instance

    if type(resource) is not str:
        raise TypeError("Resource must be a string")

    if resource is None or resource == "":
        raise AttributeError("Resource must not be empty")

    with lock:
        now = datetime.utcnow()
        now_floored = math.floor(now.timestamp())

        if lastTimestamp == now_floored:
            currentSequence += 1
        else:
            lastTimestamp = now_floored
            currentSequence = 0

    return Id(environment, resource, now, get_instance(), currentSequence)


def get_instance():
    # mac = None
    #
    # for interface in netifaces.interfaces():
    #     mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"].replace(":", "")
    #     if mac is None or mac == "" or (all_zeroes.fullmatch(mac) is not None):
    #         continue
    #     break
    #
    # if mac is not None:
    #     identifier = bytes.fromhex(mac)
    #     identifier += struct.pack(">H", os.getpid() % 65536)
    #     return Instance(Schemes.MAC_AND_PID, identifier)

    return Instance(Schemes.RANDOM, secrets.token_bytes(8))


instance = get_instance()
