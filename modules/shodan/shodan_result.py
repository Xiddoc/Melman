from dataclasses import field, dataclass
from typing import List


@dataclass
class ShodanResult:
    ip: str

    def __str__(self) -> str:
        return f"IP: {self.ip}\n" \
               f"Web: http://{self.ip}/"


@dataclass
class ShodanSearchResult:
    total: int = 0
    results: List[ShodanResult] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Total: {self.total}\n\n" \
               "Results:\n" \
               "\n".join(str(result) for result in self.results)
