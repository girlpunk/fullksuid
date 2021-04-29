from fullksuid import validation
from fullksuid.Schemes import Schemes
import struct


class Instance:
    def __init__(self, scheme: Schemes, identifier: bytes):
        validation.check_class('scheme', scheme, Schemes)
        validation.check_buffer('identifier', identifier, 8)

        self.scheme = scheme
        self.identifier = identifier
        self._buf = None

    def to_buffer(self):
        if self._buf is not None:
            return self._buf

        self._buf = b''

        self._buf += struct.pack(">B", self.scheme.value)
        self._buf += self.identifier

        return self._buf

    def __str__(self):
        return f"<Instance scheme=\"{self.scheme}\" identifier=\"{self.identifier.hex()}\">"

    @staticmethod
    def from_buffer(buffer):
        validation.check_buffer('buffer', buffer, 9)

        return Instance(
            Schemes(buffer[0]),
            buffer[1:]
        )

