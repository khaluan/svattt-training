from interfaces import MacProvider
from zlib import crc32
from os import urandom


class Crc32MP(MacProvider):
    """A MAC provider implementation using CRC32."""

    def __init__(self):
        self.secret = urandom(256)

    def get_mac_size(self) -> int:
        return 4

    def generate_mac(self, data: bytes) -> bytes:
        return (crc32(self.secret + data) % 2 ** 32).to_bytes(4, "little")

    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        return self.generate_mac(data) == mac

    def get_public_info(self) -> bytes:
        return b''
