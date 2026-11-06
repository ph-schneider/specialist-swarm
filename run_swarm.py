"""
Eigentlicher Lauf des Deal-Desk-Swarms mit frei wählbaren Eingabedaten.

Voraussetzung: einmalig `python setup_swarm.py` ausgeführt.

Usage:
    python run_swarm.py                                  # Standard: Acme-RFP
    python run_swarm.py --rfp pfad/zum/rfp.md
    python run_swarm.py --rfp rfp.md --support a.json --support b.md

Ohne --support werden die Standard-Zusatzdateien aus run_deal_desk.py genutzt
(past-wins.json, product-overview.md). Ergebnisse landen in outputs/.
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import run_deal_desk

REQUIRED_IDS = {
    ".environment_id": "setup_environment.py",
    ".specialist_ids.json": "create_specialists.py",
    ".coordinator_id": "create_coordinator.py",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--rfp", type=Path, help="Pfad zum RFP (Markdown/Text)")
    parser.add_argument(
        "--support",
        type=Path,
        action="append",
        help="Zusatzdatei als Kontext (mehrfach angebbar)",
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY fehlt. Bitte in .env eintragen.")

    missing = [f for f in REQUIRED_IDS if not Path(f).exists()]
    if missing:
        raise SystemExit(
            f"Setup unvollständig (fehlt: {', '.join(missing)}). "
            "Bitte zuerst `python setup_swarm.py` ausführen."
        )

    if args.rfp:
        if not args.rfp.exists():
            raise SystemExit(f"RFP nicht gefunden: {args.rfp}")
        run_deal_desk.RFP_PATH = args.rfp
    if args.support:
        run_deal_desk.SUPPORTING_FILES = args.support

    run_deal_desk.main()


if __name__ == "__main__":
    main()
