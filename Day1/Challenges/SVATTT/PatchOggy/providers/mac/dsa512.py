from interfaces import MacProvider
from random import randint
import time

p = 0x299279f0e8cafde76b4377a707943c616f734b60c0d1817f105a1b739688b94a81ed4b77275f588910fd3562a8c52ee8cd69cb9b3696c3af80b7a8b7f28944b
h = 2
q = (p - 1) // h
g = pow(2021, h, p)


class Dsa512MP(MacProvider):
    """A MAC provider implementation using DSA."""

    def __init__(self):
        self.x = randint(1, q - 1)
        self.y = pow(g, self.x, p)

    def get_mac_size(self) -> int:
        return 128

    def generate_mac(self, data: bytes) -> bytes:
        m = int.from_bytes(data, "big")
        k = int(time.time())
        r = pow(g, k, p) % q
        s = pow(k, -1, q) * (m + self.x * r) % q
        return r.to_bytes(64, "big") + s.to_bytes(64, "big")

    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        m = int.from_bytes(data, "big")
        r = int.from_bytes(mac[:64], "big");assert r>0
        s = int.from_bytes(mac[64:], "big")
        w = pow(s, -1, q)
        u1 = m * w % q
        u2 = r * w % q
        v = pow(g, u1, p) * pow(self.y, u2, p) % p % q
        return v == r

    def get_public_info(self) -> bytes:
        return hex(self.y).encode()
