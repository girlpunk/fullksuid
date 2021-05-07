import os
import sys
from datetime import datetime
import struct
import netifaces
import random
import math
import re
import threading

from fullksuid import validation
from fullksuid.Instance import Instance
from fullksuid.Id import Id
from fullksuid.Schemes import Schemes

this = sys.modules[__name__]

this.environment = ""

this.lastTimestamp = 0
this.currentSequence = 0
this.lock = threading.Lock()

all_zeroes = re.compile(r"^0+$")


def get_environment() -> str:
    return this.environment


def set_environment(value: str):
    validation.check_prefix('environment', value)
    this.environment = value


def generate(resource: str) -> Id:
    if type(resource) is not str:
        raise TypeError("Resource must be a string")

    if resource is None or resource == "":
        raise AttributeError("Resource must not be empty")

    with this.lock:
        now = datetime.utcnow()
        now_floored = math.floor(now.timestamp())

        if this.lastTimestamp == now_floored:
            this.currentSequence += 1
        else:
            this.lastTimestamp = now_floored
            this.currentSequence = 0

    return Id(this.environment, resource, now, this.instance, this.currentSequence)


def get_instance():
    mac = None

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

    return Instance(Schemes.RANDOM, random.randbytes(8))


this.instance = get_instance()
