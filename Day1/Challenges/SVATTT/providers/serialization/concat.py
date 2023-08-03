from interfaces import SerializationProvider
from typing import Dict


class ConcatenatorSP(SerializationProvider):
    """A simple serialization provider implementation using string
    concatenation."""

    def serialize(self, info: Dict[bytes, bytes]) -> bytes:
        result = []
        for k, v in info.items():
            assert b'|' not in k
            assert b'|' not in v
            result.append(k)
            result.append(v)
        return b'|'.join(result)

    def deserialize(self, data: bytes) -> Dict[bytes, bytes]:
        result = {}
        k = None
        for s in data.split(b'|'):
            if k is None:
                k = s
            else:
                result[k] = s
                k = None
        return result
