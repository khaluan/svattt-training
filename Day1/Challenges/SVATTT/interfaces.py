from abc import ABC, abstractmethod
from typing import Dict


class MacProvider(ABC):
    """Interface for a MAC (message authentication code) service provider."""

    @abstractmethod
    def get_mac_size(self) -> int:
        pass

    @abstractmethod
    def generate_mac(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        pass

    @abstractmethod
    def get_public_info(self) -> bytes:
        """Return the information needed for publicly verifying generated
        MACs. In case the feature is not supported, an empty `bytes` should be
        returned."""
        pass


class SerializationProvider(ABC):
    """Interface for a serialization service provider."""

    @abstractmethod
    def serialize(self, info: Dict[bytes, bytes]) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Dict[bytes, bytes]:
        pass
