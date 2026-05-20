from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class AssetManifest:
    version: int = 1
    attempts: list[dict[str, Any]] = field(default_factory=list)

    def add_attempt(
        self,
        *,
        item_id: str,
        stage: str,
        status: str,
        output_path: str,
    ) -> None:
        self.attempts.append(
            {
                "item_id": item_id,
                "stage": stage,
                "status": status,
                "output_path": output_path,
                "created_at": datetime.now(UTC).isoformat(),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "attempts": self.attempts,
        }
