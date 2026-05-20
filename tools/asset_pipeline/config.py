from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    def __post_init__(self):
        object.__setattr__(self, "root", Path(self.root).resolve())

    @property
    def data_items(self) -> Path:
        return self.root / "data" / "items"

    @property
    def prompts(self) -> Path:
        return self.root / "data" / "prompts"

    @property
    def concepts(self) -> Path:
        return self.root / "assets" / "concepts"

    @property
    def models_raw(self) -> Path:
        return self.root / "assets" / "models_raw"

    @property
    def models_processed(self) -> Path:
        return self.root / "assets" / "models_processed"

    @property
    def review(self) -> Path:
        return self.root / "assets" / "review"

    @property
    def manifests(self) -> Path:
        return self.root / "data" / "manifests"

    def ensure_generated_dirs(self) -> None:
        for path in (
            self.data_items,
            self.concepts,
            self.models_raw,
            self.models_processed,
            self.review,
            self.manifests,
        ):
            path.mkdir(parents=True, exist_ok=True)
