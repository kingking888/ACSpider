import base64
import hashlib


def Base64Encode(string):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def Base64Decode(string):
    ab64_string = string.replace("\n", "")
    return base64.b64decode(ab64_string)


def md5_string(string):
    return hashlib.md5(string.encode()).hexdigest()
