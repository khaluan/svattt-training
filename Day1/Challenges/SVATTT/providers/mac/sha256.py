from interfaces import MacProvider
from hashlib import sha256
from os import urandom


class Sha256MP(MacProvider):
    """A MAC provider implementation using SHA-256."""

    def __init__(self):
        self.secret = urandom(32)

    def get_mac_size(self) -> int:
        return 32

    def generate_mac(self, data: bytes) -> bytes:
        return sha256(self.secret + data).digest()

    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        return self.generate_mac(data) == mac

    def get_public_info(self) -> bytes:
        return b''
