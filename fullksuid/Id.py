import struct
import base62
import math
from datetime import datetime

from fullksuid.Instance import Instance
from fullksuid import validation


decodedLen = 21
encodedLen = 29
alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

class Id:
    def __init__(self, environment: str, resource: str, timestamp: datetime, instance: Instance, sequence_id: int):
        if environment is None or environment == "":
            environment = "prod"
        validation.check_prefix('environment', environment)
        validation.check_prefix('resource', resource)
        validation.check_class('timestamp', timestamp, datetime)
        validation.check_class('instance', instance, Instance)
        validation.check_uint('sequenceId', sequence_id, 4)

        self.environment = environment
        self.resource = resource
        self.timestamp = timestamp
        self.instance = instance
        self.sequenceId = sequence_id

        self._str = None

    def __str__(self):
        # immutable, so cache
        if self._str is not None:
            return self._str

        if self.environment == "prod":
            prefix = f"{self.resource}_"
        else:
            prefix = f"{self.environment}_{self.resource}_"

        decoded = b''

        decoded += struct.pack(">I", math.floor(self.timestamp.timestamp()))
        decoded += self.instance.to_buffer()
        decoded += struct.pack(">I", self.sequenceId)

        encoded = base62.encodebytes(decoded, alphabet).rjust(encodedLen, '0')

        self._str = prefix + encoded

        return self._str

    @staticmethod
    def parse(value: str):
        validation.check_class("value", value, str)
        if value is None or value == "":
            raise ValueError('value must not be empty')

        environment, resource, encoded = split_prefix_id(value)
        decoded: bytes = base62.decodebytes(encoded, alphabet)

        return Id(
            environment,
            resource,
            datetime.utcfromtimestamp(struct.unpack_from(">I", decoded)[0]),
            Instance.from_buffer(decoded[4:13]),
            struct.unpack_from(">I", decoded, 13)[0]
        )


def split_prefix_id(value: str):
    parsed = validation.ksuidRegex.fullmatch(value)

    if not parsed:
        raise ValueError("ID is invalid")

    environment, resource, encoded = parsed.groups()

    if environment is None:
        environment = "prod"

    return environment, resource, encoded
