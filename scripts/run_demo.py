"""Run an end-to-end demo over sample reimbursement claims."""

import asyncio
import json
import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agents.reimbursement_agent import ReimbursementAgent
from app.constants import CLAIMS_DIR, OUTPUT_DIR

logging.basicConfig(level=logging.WARNING) # reduce noise
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

async def run() -> list[dict[str, object]]:
    """Evaluate sample claims and write sample outputs."""
    agent = ReimbursementAgent()
    output_dir = OUTPUT_DIR / "sample_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    
    print("\nEvaluating claims...\n")
    for claim_path in sorted(Path(CLAIMS_DIR).glob("*.json")):
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        print(f"Processing {claim['claim_id']} ({claim['category']}) - {claim['amount']} {claim['currency']}")
        
        result = await agent.evaluate_claim(claim)
        results.append(result)
        
        output_path = output_dir / f"{claim['claim_id']}_decision.json"
        output_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
        
    return results


def print_summary(results: list[dict[str, object]]) -> None:
    """Print a readable ASCII table of the results."""
    print("\n" + "="*80)
    print(f"{'CLAIM ID':<12} | {'DECISION':<18} | {'APP. AMT':<10} | {'REJ. AMT':<10} | {'CONF':<5}")
    print("-" * 80)
    for r in results:
        decision = str(r.get('decision', 'N/A'))
        app_amt = f"${float(str(r.get('approved_amount', 0))):.2f}"
        rej_amt = f"${float(str(r.get('rejected_amount', 0))):.2f}"
        conf = f"{float(str(r.get('confidence', 0))):.2f}"
        print(f"{str(r['claim_id']):<12} | {decision:<18} | {app_amt:<10} | {rej_amt:<10} | {conf:<5}")
    print("="*80 + "\n")


def main() -> None:
    """Run a demo workflow."""
    results = asyncio.run(run())
    print_summary(results)
    print(f"Detailed JSON results written to {OUTPUT_DIR / 'sample_outputs'}")


if __name__ == "__main__":
    main()
