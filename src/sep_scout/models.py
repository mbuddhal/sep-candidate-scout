from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Candidate:
    name: str
    grad_signal: str = ""
    major_area: str = ""
    public_signal: str = ""
    fit_angle: str = ""
    cutoff_status: str = "Needs verification"
    source_type: str = "Public web"
    source_url: str = ""
    score: int = 0
    roles: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def sheet_row(self) -> list[str]:
        return [
            self.name,
            self.grad_signal,
            self.major_area,
            self.public_signal,
            self.fit_angle,
            self.cutoff_status,
            self.source_type,
            self.source_url,
        ]
