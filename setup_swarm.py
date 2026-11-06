"""
Einmaliges (bzw. seltenes) Setup des Deal-Desk-Swarms.

Führt die Setup-Schritte in der richtigen Reihenfolge aus und überspringt
Schritte, die bereits erledigt sind (erkennbar an den ID-Dateien):

    1. setup_environment.py   -> .environment_id
    2. create_specialists.py  -> .specialist_ids.json
    3. upload_skills.py       -> .skill_ids.json (Skills hochladen + anhängen)
    4. create_coordinator.py  -> .coordinator_id

Der eigentliche Lauf mit Eingabedaten startet danach mit run_swarm.py.

Usage:
    python setup_swarm.py            # fehlende Schritte nachholen
    python setup_swarm.py --force    # Specialists + Coordinator neu anlegen
                                     # (Environment bleibt erhalten)
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import create_coordinator
import create_specialists
import setup_environment
import upload_skills


def step(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--force",
        action="store_true",
        help="Specialists und Coordinator neu anlegen (alte IDs werden verworfen)",
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY fehlt. Bitte in .env eintragen.")

    if args.force:
        for name in (".specialist_ids.json", ".coordinator_id"):
            Path(name).unlink(missing_ok=True)
        print("--force: alte Specialist-/Coordinator-IDs verworfen.")

    step("1/4 Environment")
    setup_environment.main()  # überspringt sich selbst, wenn .environment_id existiert

    step("2/4 Specialists")
    if Path(".specialist_ids.json").exists():
        print("Bereits vorhanden (.specialist_ids.json) — übersprungen.")
    else:
        create_specialists.main()

    step("3/4 Skills")
    upload_skills.main()  # idempotent: nutzt vorhandene Skills wieder

    step("4/4 Coordinator")
    if Path(".coordinator_id").exists():
        print("Bereits vorhanden (.coordinator_id) — übersprungen.")
    else:
        create_coordinator.main()

    print("\nSetup abgeschlossen. Lauf starten mit: python run_swarm.py")


if __name__ == "__main__":
    sys.exit(main())
