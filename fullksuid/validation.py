import re


ksuidRegex = re.compile(r"^(?:([a-z\d]+)_)?([a-z\d]+)_([a-zA-Z\d]{29})$")
prefixRegex = re.compile(r"^[a-z\d]+$")


def check_prefix(field: str, value: str):
    if type(value) is not str:
        raise TypeError(f"{field} must be a string")

    if prefixRegex.fullmatch(value):
        return

    raise ValueError(f"{field} contains invalid characters")


def check_uint(field: str, value: int, byte_length: int):
    if type(value) is not int:
        raise TypeError(f"{field} must be an integer")

    if value < 0:
        raise ValueError(f"{field} must be positive")

    if value >= pow(2, byte_length * 8):
        raise ValueError(f"{field} must be a uint${byte_length * 8}")


def check_buffer(field: str, value: bytes, byte_length: int):
    if type(value) is not bytes:
        raise TypeError(f"{field} must be bytes")

    if len(value) != byte_length:
        raise ValueError(f"{field} must be ${byte_length} bytes")


def check_class(field: str, value, class_type: type):
    if type(value) is not class_type:
        raise TypeError(f"{field} must be an instance of ${class_type}")
