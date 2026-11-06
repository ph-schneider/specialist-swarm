# Verwendung: Setup und Lauf des Deal-Desk-Swarms

Diese Anleitung beschreibt, wie der Swarm für Card A (Deal Desk) eingerichtet und gestartet wird. Der Ablauf besteht aus zwei Teilen:

| Teil | Skript | Häufigkeit |
| --- | --- | --- |
| Setup | [setup_swarm.py](../setup_swarm.py) | einmalig bzw. selten |
| Lauf mit Eingabedaten | [run_swarm.py](../run_swarm.py) | beliebig oft |

## 1. Voraussetzungen

1. **Virtuelle Umgebung** mit den Abhängigkeiten (einmalig):
   ```bash
   python -m venv .venv
   .venv/Scripts/python -m pip install -r requirements.txt
   ```
2. **Virtuelle Umgebung aktivieren:**
   - Git Bash: `source .venv/Scripts/activate`
   - PowerShell: `.venv\Scripts\Activate.ps1`
   - cmd: `.venv\Scripts\activate.bat`
3. **API-Key** in einer Datei `.env` im Projektordner:
   ```
   ANTHROPIC_API_KEY=dein-key-hier
   ```
   Die `.env` ist in der [.gitignore](../.gitignore) eingetragen und wird nicht committet. Den Schlüssel bitte nicht in Chats, Code oder Commits teilen.
4. **Workspace-Zugriff:** Managed Agents Multi-Agent ist laut README eine Research Preview. Der Workspace braucht dafür Zugriff.

Alle Befehle unten werden im Projektordner ausgeführt.

## 2. Setup (einmalig)

```bash
python setup_swarm.py
```

Das Skript führt diese Schritte in fester Reihenfolge aus:

| Schritt | Aktion | Ergebnisdatei |
| --- | --- | --- |
| 1 | Cloud-Environment anlegen | `.environment_id` |
| 2 | Vier Specialists anlegen | `.specialist_ids.json` |
| 3 | Skills hochladen und an die Specialists anhängen | `.skill_ids.json` |
| 4 | Coordinator anlegen | `.coordinator_id` |

**Wiederholbar:** Schritte, deren Ergebnisdatei schon existiert, werden übersprungen. Ein erneuter Aufruf legt nichts doppelt an. Der Skill-Upload erkennt bereits vorhandene Skills selbst.

### Option `--force`

```bash
python setup_swarm.py --force
```

Verwirft die Specialist- und Coordinator-IDs und legt beide neu an. Das Environment bleibt erhalten. Sinnvoll, wenn sich Prompts, Modelle oder die Roster-Zusammensetzung geändert haben.

### Neuen Skill nachträglich ergänzen

1. Skill-Ordner mit `SKILL.md` unter `skills/<name>/` ablegen.
2. In `SKILL_TO_SPECIALIST` in [upload_skills.py](../upload_skills.py) den Eintrag `"<name>": "<specialist-key>"` ergänzen. Die Specialist-Keys sind `pricing`, `legal`, `technical_fit` und `competitive`.
3. `python upload_skills.py` ausführen oder `python setup_swarm.py` erneut starten. Vorhandene Skills werden wiederverwendet.

## 3. Lauf mit Eingabedaten

```bash
python run_swarm.py
```

Ohne Argumente verwendet der Lauf die Standarddaten:
- RFP: `synthetic-data/rfp-acme-corp.md`
- Zusatzdateien: `synthetic-data/past-wins.json`, `synthetic-data/product-overview.md`

### Eigene Eingabedaten

| Option | Bedeutung |
| --- | --- |
| `--rfp <Pfad>` | Pfad zum RFP (Markdown oder Text) |
| `--support <Pfad>` | Zusatzdatei als Kontext, mehrfach angebbar |

Beispiele:
```bash
python run_swarm.py --rfp mein-rfp.md
python run_swarm.py --rfp mein-rfp.md --support preise.json --support produkt.md
```

Wenn `--support` angegeben wird, ersetzt es die Standard-Zusatzdateien. Soll `past-wins.json` oder `product-overview.md` weiter genutzt werden, muss die Datei erneut angegeben werden.

### Was beim Lauf passiert

1. Der Lauf prüft, ob das Setup vollständig ist. Sonst erscheint ein Hinweis auf `setup_swarm.py`.
2. RFP und Zusatzdateien werden in die Nachricht an den Coordinator eingebettet.
3. Der Coordinator delegiert parallel an die vier Specialists. Der Event-Stream zeigt das live:
   - `[thread spawned]`, `[thread running]`
   - `[delegate →]` und `[reply ←]`
   - `[tool: ...]`
4. Am Ende werden die Ergebnisse in `outputs/` gespeichert und ein Link zur Session ausgegeben.

### Ergebnisse

| Datei | Inhalt |
| --- | --- |
| `outputs/coordinator-transcript.txt` | Textausgabe des Coordinators |
| `outputs/<Dateiname>` | alle Dateien, die die Agents im Container erzeugt haben |
| `.last_session_id` | ID der letzten Session |

Die Ausgabe ist ein generierter Entwurf. Vor jeder externen Verwendung muss sie fachlich geprüft und freigegeben werden.

## 4. Übersicht der Dateien

| Datei | Zweck |
| --- | --- |
| [setup_swarm.py](../setup_swarm.py) | Setup in einem Schritt (Einstiegspunkt) |
| [run_swarm.py](../run_swarm.py) | Lauf mit Eingabedaten (Einstiegspunkt) |
| [setup_environment.py](../setup_environment.py) | Einzelschritt: Environment |
| [create_specialists.py](../create_specialists.py) | Einzelschritt: Specialists |
| [upload_skills.py](../upload_skills.py) | Einzelschritt: Skills |
| [create_coordinator.py](../create_coordinator.py) | Einzelschritt: Coordinator |
| [run_deal_desk.py](../run_deal_desk.py) | Der eigentliche Lauf, von `run_swarm.py` aufgerufen |

Die Einzelschritte lassen sich auch separat starten, etwa zur Fehlersuche.

## 5. Fehlerbehebung

| Meldung oder Symptom | Ursache und Lösung |
| --- | --- |
| `ANTHROPIC_API_KEY fehlt` | `.env` fehlt oder ist leer. Key eintragen und aus dem Projektordner starten. |
| `Setup unvollständig (fehlt: ...)` | `python setup_swarm.py` ausführen. |
| Fehler beim Anlegen der Agents (Modell, Header, Tool-Typ) | Modellnamen, Beta-Header `managed-agents-2026-04-01` und Tool-Typ `agent_toolset_20260401` sind im Code fest eingetragen und im Workspace zu prüfen. |
| Fehler beim Coordinator (Multi-Agent) | Workspace hat keinen Zugriff auf die Research Preview. Workspace-Admin ansprechen. |
| Kein `.docx` in `outputs/` | Erwartet, solange das docx-Skill nicht am Coordinator angehängt ist. Der Coordinator liefert dann Markdown (siehe [Analyse](00-inital-requirement-analysis.md), Lücke L2). |
| Änderungen an Prompts wirken nicht | Specialists und Coordinator sind bereits angelegt. `python setup_swarm.py --force` ausführen. |

## 6. Hinweis

Die Skripte `setup_swarm.py` und `run_swarm.py` wurden bisher nur auf Syntax und `--help` geprüft. Ein vollständiger Lauf gegen die API steht noch aus.
