from interfaces import MacProvider
from os import urandom
from Crypto.Cipher import AES  # pycryptodome
from Crypto.Util.strxor import strxor


class Aes256XorMP(MacProvider):
    """A MAC provider implementation using AES and XOR."""

    def __init__(self):
        self.secret = urandom(32)

    def get_mac_size(self) -> int:
        return 16

    def generate_mac(self, data: bytes) -> bytes:
        # padding
        data += b'\x00' * (-len(data) % 16)

        # encrypting
        enc_data = AES.new(self.secret, mode=AES.MODE_ECB).encrypt(data)

        # xor-ing
        result = bytearray(16)
        for i in range(0, len(enc_data), 16):
            strxor(result, enc_data[i: i + 16], result)

        return bytes(result)

    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        return self.generate_mac(data) == mac

    def get_public_info(self) -> bytes:
        return b''
