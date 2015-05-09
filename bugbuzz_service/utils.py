"""From https://bitcointalk.org/index.php?topic=1026.0

by Gavin Andresen (public domain)

"""
from __future__ import unicode_literals
import uuid

B58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B58_BASE = len(B58_CHARS)


def b58encode(s):
    value = 0
    for i, c in enumerate(reversed(s)):
        value += ord(c) * (256 ** i)

    result = []
    while value >= B58_BASE:
        div, mod = divmod(value, B58_BASE)
        c = B58_CHARS[mod]
        result.append(c)
        value = div
    result.append(B58_CHARS[value])
    return ''.join(reversed(result))


class GUIDFactory(object):
    """Object for making prefixed GUID

    """

    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self):
        return self.prefix + b58encode(uuid.uuid4().bytes)
