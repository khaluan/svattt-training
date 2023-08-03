from interfaces import MacProvider, SerializationProvider
from typing import Dict


class CovidVaccinationCertificateBuilder:
    """
    For building/parsing certificates of COVID vaccination for citizens.
    """

    def __init__(self, mp: MacProvider, sp: SerializationProvider):
        self.mac_size = mp.get_mac_size()
        self.mp = mp
        self.sp = sp
        self.issuer = b""
        self.citizen_id = b""
        self.citizen_name = b""

    def set_issuer(self, issuer: bytes):
        self.issuer = issuer

    def set_citizen(self, citizen_id: bytes, citizen_name: bytes):
        self.citizen_id = citizen_id
        self.citizen_name = citizen_name

    def _get_vaccination_status(self) -> int:
        """Get number of COVID vaccine doses taken by the target citizen."""
        assert self.citizen_id != b""
        assert self.citizen_name != b""

        # The national vaccination database is not open.
        # We're sorry about that...
        return 0

    def build(self) -> bytes:
        """Build a certificate with information already provided via set_*
        methods."""
        doses = self._get_vaccination_status()
        data = self.sp.serialize({
            b"issuer": self.issuer,
            b"citizen_id": self.citizen_id,
            b"citizen_name": self.citizen_name,
            b"doses": doses.to_bytes(1, "big")  # hopefully no one will take
            # more than 255 doses :D
        })
        mac = self.mp.generate_mac(data)
        return data + mac

    def parse(self, certificate: bytes) -> Dict[bytes, bytes]:
        """Parse a certificate."""
        data = certificate[:-self.mac_size]
        mac = certificate[-self.mac_size:]
        assert self.mp.verify_mac(data, mac)
        return self.sp.deserialize(data)
    def debug(self, data):
        return b"[DEBUG]" + self.mp.generate_mac(data)