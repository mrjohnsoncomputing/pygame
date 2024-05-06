from dataclasses import dataclass
from socket import gethostbyname, gethostname

@dataclass
class Address:
    ipv4: str
    port: int

    @classmethod
    def from_dynamic_ipv4(cls, port: int):
        return cls(
            ipv4 = gethostbyname(gethostname()),
            port=port
        )
    
    @property
    def tuple(self) -> tuple[str, int]:
        return (self.ipv4, self.port)

    def __str__(self) -> str:
        return f"{self.ipv4}:{self.port}"