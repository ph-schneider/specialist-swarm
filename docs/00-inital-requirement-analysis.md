# Initiale Anforderungsanalyse — Card A (Deal Desk)

| | |
| --- | --- |
| **Szenario** | Card A — Deal Desk (siehe [scenario-cards.md](../scenario-cards.md)) |
| **Stand** | 2026-11-06 |
| **Grundlage** | Statische Code-Analyse des Repositories. Es wurde nichts gegen die API ausgeführt. |
| **Status** | Entwurf, zur Abstimmung im Team |

## 1. Executive Summary

Card A ist im Starter-Code weitgehend vorverdrahtet: Specialists, Coordinator, Environment, Skill-Upload und der Lauf mit Event-Stream sind vorhanden. Die Pipeline ist aber noch **nicht lauffähig bis zum Ziel-Deliverable** `outputs/proposal-response.docx`.

Die wichtigsten Lücken:

1. Für den Technical-Fit-Specialist existiert kein Skill (`product-overview`).
2. Das vorgebaute docx-Skill ist nirgends angehängt, der Coordinator fällt voraussichtlich auf Markdown zurück.
3. Ein im Prompt referenzierter Branding-Skill existiert nicht.
4. Der Dateiname des Deliverables ist nicht festgelegt.
5. Die Reihenfolge der Setup-Schritte ist in README und Skripten uneinheitlich.

Zusätzlich sind mehrere Konfigurationswerte (Modelle, Beta-Header) ungeprüft. Details und offene Entscheidungen stehen in den Abschnitten 4 und 5.

## 2. Ziel laut Card A

- **Coordinator:** "Senior Partner — Deal Desk Lead". Er liest den RFP, delegiert und erstellt ein gebrandetes Antwortdokument.
- **Specialists:**
  1. Pricing Specialist (Skill: `pricing-playbook`)
  2. Legal Reviewer (Skill: `legal-checklist`)
  3. Technical Fit (Skill: `product-overview`)
  4. Competitive Intel (Skill: `competitive-intel`)
- **Trigger:** `synthetic-data/rfp-acme-corp.md`
- **Deliverable:** Word-Dokument `outputs/proposal-response.docx`

## 3. Bestandsaufnahme

| Baustein | Datei | Stand |
| --- | --- | --- |
| Cloud-Environment anlegen | [setup_environment.py](../setup_environment.py) | vorhanden |
| 4 Specialists mit Rollen-Prompts | [create_specialists.py](../create_specialists.py) | vorhanden |
| Coordinator mit `multiagent: coordinator` und Roster | [create_coordinator.py](../create_coordinator.py) | vorhanden |
| Skill-Upload und Anhängen an Specialists (mehrfach ausführbar) | [upload_skills.py](../upload_skills.py) | 3 von 4 Skills |
| Lauf mit Event-Stream, Transcript, Datei-Download | [run_deal_desk.py](../run_deal_desk.py) | vorhanden |
| Eingabedaten (RFP, `past-wins.json`, `product-overview.md`) | [synthetic-data/](../synthetic-data/) | vorhanden |
| Skills `pricing-playbook`, `legal-checklist`, `competitive-intel` | [skills/](../skills/) | vorhanden |
| API-Key über `.env` (`load_dotenv()` in allen Skripten) | alle Skripte | umgesetzt |
| Virtuelle Umgebung `.venv` mit `requirements.txt` | Projektwurzel | umgesetzt |

## 4. Lücken und Erweiterungsbedarf

### L1 — Technical-Fit-Skill fehlt

- **Befund:** Die Card nennt den Skill `product-overview`. Vorhanden ist nur die Datei `synthetic-data/product-overview.md`, aber kein Ordner `skills/product-overview/SKILL.md`. In `SKILL_TO_SPECIALIST` ([upload_skills.py](../upload_skills.py)) fehlt der Eintrag.
- **Auswirkung:** Der Specialist erhält die Produktinformationen nur indirekt über die Nachricht des Coordinators. Das widerspricht dem Skill-Konzept der Card.
- **Maßnahme:** `skills/product-overview/SKILL.md` mit Frontmatter (`name`, `description`) aus der Produktübersicht erstellen. Den Eintrag `"product-overview": "technical_fit"` in `SKILL_TO_SPECIALIST` ergänzen.

### L2 — docx-Skill ist nicht angebunden

- **Befund:** Der Coordinator wird ohne `skills` erstellt. [upload_skills.py](../upload_skills.py) hängt nur eigene Skills an die Specialists. Der Coordinator-Prompt sagt "docx skill falls verfügbar, sonst Markdown".
- **Auswirkung:** Voraussichtlich entsteht kein `.docx`, sondern ein Markdown-Fallback. Das Ziel-Deliverable wird verfehlt.
- **Maßnahme:** Das vorgebaute docx-Skill beim Coordinator anhängen. Den Prompt auf "muss ein `.docx` erzeugen" schärfen.

### L3 — Branding-Skill ist referenziert, existiert aber nicht

- **Befund:** [create_coordinator.py](../create_coordinator.py) erwähnt einen "BTS branding skill". Er ist im Repository nicht vorhanden.
- **Auswirkung:** Der Verweis läuft ins Leere. Das Dokument wäre nicht "gebrandet" im Sinne der Card.
- **Maßnahme:** Entscheidung nötig, siehe O1. Entweder einen Branding- oder Firm-Voice-Skill ergänzen oder den Verweis entfernen.

### L4 — Dateiname des Deliverables nicht festgelegt

- **Befund:** [run_deal_desk.py](../run_deal_desk.py) speichert jede Datei unter dem Namen, den der Agent gewählt hat. Der Coordinator-Prompt nennt keinen Dateinamen.
- **Auswirkung:** `outputs/proposal-response.docx` ist nicht garantiert.
- **Maßnahme:** Den Dateinamen `proposal-response.docx` im Coordinator-Prompt vorgeben. Optional nach dem Download prüfen oder umbenennen.

### L5 — Uneinheitliche Reihenfolge der Setup-Schritte

- **Befund:** Die README nennt Specialists, Coordinator, Skills. Die Fehlermeldung in [run_deal_desk.py](../run_deal_desk.py) nennt Specialists, Skills, Coordinator. `setup_environment.py` fehlt in der README, obwohl `.environment_id` Pflicht ist.
- **Auswirkung:** Verwirrung bei der Ausführung. Mögliches Versionsproblem, siehe O3.
- **Maßnahme:** Eine verbindliche Reihenfolge festlegen und in README, Docstrings und Fehlermeldungen angleichen.

### L6 — Konfigurationswerte sind ungeprüft

- **Befund:** Fest im Code stehen die Modelle `claude-sonnet-4-6`, `claude-opus-4-7` und `claude-haiku-4-5-20251001`, der Beta-Header `managed-agents-2026-04-01` und der Tool-Typ `agent_toolset_20260401`.
- **Auswirkung:** Falls ein Wert im Workspace ungültig ist, schlägt die Erstellung fehl. Das wird erst beim ersten Lauf sichtbar.
- **Maßnahme:** Beim ersten Lauf prüfen. Die Modelle gegebenenfalls zentral konfigurierbar machen.

## 5. Offene Punkte

| ID | Offener Punkt | Warum es wichtig ist | Vorschlag | Entscheider |
| --- | --- | --- | --- | --- |
| O1 | Soll es ein eigenes Firm-Branding geben (z. B. Capgemini-nahe Gestaltung), oder reicht das Standard-docx? | Bestimmt, ob ein zusätzlicher Branding-Skill nötig ist (L3). | Zunächst Standard-docx, Branding als Erweiterung. | Team |
| O2 | Hat der Workspace Zugriff auf Managed Agents Multi-Agent (Research Preview)? | Ohne Zugriff schlägt die Coordinator-Erstellung fehl. | Früh mit `create_specialists.py` testen. | Team / Workspace-Admin |
| O3 | Sieht der Coordinator Specialists nach dem Skill-Update in der aktuellen Version? | [upload_skills.py](../upload_skills.py) ändert Specialists nach dem Anlegen des Coordinators (siehe L5). | Reihenfolge so wählen, dass Skills vor dem Coordinator angehängt werden, und beim ersten Lauf prüfen. | Team |
| O4 | Sind Modelle, Beta-Header und Tool-Typ im Workspace gültig? | Siehe L6. | Beim ersten Lauf prüfen und dokumentieren. | Team |
| O5 | Wie gelangen `past-wins.json` und `product-overview.md` zu den Specialists? | Aktuell stehen sie in der Nachricht an den Coordinator, der sie weiterreichen muss. | Für das Produktwissen löst L1 das Problem. Für `past-wins.json` ist zu klären, ob der Coordinator-Weg reicht. | Team |
| O6 | Welche Datenklassifizierung gilt für die Eingabedaten? | Die Daten sind synthetisch. Bei Übertragung echter Kunden- oder Preisdaten in die Cloud gelten Vertraulichkeits- und Datenschutzvorgaben. | Vor dem Einsatz echter Daten den Data Privacy Officer einbinden. | Data Privacy Officer / Compliance |
| O7 | Wie wird das Ergebnis qualitätsgesichert? | Das Deliverable ist für eine externe Verwendung gedacht und nicht automatisch fachlich geprüft. | Vor Weitergabe fachliche Prüfung durch Pricing, Legal und Delivery. Optional Critic-Agent (siehe [stretch-goals.md](../stretch-goals.md)). | Team |
| O8 | Ist `.env.example` bereit zum Commit? | Die Datei liegt untracked im Repository. Ihr Inhalt wurde nicht geprüft. | Prüfen, dass nur Platzhalter enthalten sind, dann committen. | Team |

## 6. Empfohlene nächste Schritte

1. **O1 klären** (Branding ja oder nein).
2. **L1 umsetzen:** Skill `product-overview` anlegen und zuordnen.
3. **L2 bis L4 umsetzen:** docx-Skill am Coordinator, Branding-Verweis klären, Dateiname festschreiben.
4. **L5 umsetzen:** Reihenfolge in README, Docstrings und Fehlermeldungen vereinheitlichen.
5. **Lauf durchführen** in dieser Reihenfolge, vorbehaltlich O3:
   `setup_environment.py`, `create_specialists.py`, `upload_skills.py`, `create_coordinator.py`, `run_deal_desk.py`.
6. **Ergebnis prüfen:** Event-Stream, `outputs/proposal-response.docx` und die offenen Punkte O2 bis O5 abhaken.

## 7. Hinweis

Das Ergebnis des Swarms ist ein generierter Entwurf. Vor jeder externen Verwendung, etwa als Antwort an einen Kunden, muss es fachlich geprüft und freigegeben werden.
