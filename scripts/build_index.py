"""Build a lightweight policy index artifact for local retrieval demos."""

import json
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.constants import POLICY_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)


def main() -> None:
    """Build the policy vector index."""
    # TODO: Replace keyword chunks with real embeddings and FAISS persistence.
    policy_text = (POLICY_DIR / "travel_policy.md").read_text(encoding="utf-8")
    chunks = [
        {"chunk_id": f"policy-{idx}", "text": line.strip()}
        for idx, line in enumerate(policy_text.splitlines(), 1)
        if line.strip() and not line.startswith("#")
    ]
    output_dir = PROJECT_ROOT / "vector_store" / "embeddings"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "policy_chunks.json").write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    Path(PROJECT_ROOT / "vector_store" / "faiss_index" / ".gitkeep").touch()
    print(f"Indexed {len(chunks)} policy chunks.")


if __name__ == "__main__":
    main()
