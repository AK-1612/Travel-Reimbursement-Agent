"""Clean generated demo artifacts."""

import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.constants import OUTPUT_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)


def main() -> None:
    """Clean generated artifacts."""
    # TODO: Add a dry-run mode and preserve selected audit artifacts.
    for directory in [OUTPUT_DIR / "audit_logs", OUTPUT_DIR / "sample_outputs", PROJECT_ROOT / "vector_store" / "embeddings"]:
        for path in Path(directory).glob("*.json"):
            path.unlink()
    print("Generated JSON artifacts removed.")


if __name__ == "__main__":
    main()
