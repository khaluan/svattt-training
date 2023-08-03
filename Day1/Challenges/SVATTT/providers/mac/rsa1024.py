from interfaces import MacProvider
from Crypto.Util.number import getPrime, GCD  # pycryptodome


class Rsa1024MP(MacProvider):
    """A MAC provider implementation using RSA."""

    def __init__(self):
        self.e = e = 0x2021
        p = q = 1
        while GCD(p - 1, e) > 1:
            p = getPrime(512)
        while GCD(q - 1, e) > 1:
            q = getPrime(512)
        self.n = p * q
        self.d = pow(self.e, -1, (p - 1) * (q - 1))

    def get_mac_size(self) -> int:
        return 128

    def generate_mac(self, data: bytes) -> bytes:
        m = int.from_bytes(data, "big") % self.n
        s = pow(m, self.d, self.n)
        return s.to_bytes(128, "big")

    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        m = int.from_bytes(data, "big") % self.n
        s = int.from_bytes(mac, "big") % self.n
        return pow(s, self.e, self.n) == m

    def get_public_info(self) -> bytes:
        return ','.join(hex(x) for x in (self.n, self.e, self.d)).encode()
