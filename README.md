# Scheme Sathi — AI02 Multilingual Government Scheme Assistant

Software-only prototype for STARTUP TN24 problem statement **AI02** ("Multilingual Government Scheme Assistant"). Tamil-first, English toggle, no hardware, no personal data collection.

## Run

```powershell
cd C:\Users\voice\Downloads\STARTUP\scheme_sathi
py -m pip install -r requirements.txt   # Flask is already installed on this machine
py app.py
```

Open <http://127.0.0.1:5000>.

## Test

```powershell
py -m unittest discover -s tests -v
```

16 tests cover data completeness, official-domain allowlisting, Tamil/English intent detection, search, address answers, all web routes, `/ask`, and privacy checks.

## Features

- 5 verified schemes: **KMUT, PM-Kisan, PM MUDRA Yojana, DAY-NRLM women's SHGs, Sukanya Samriddhi Yojana**.
- Search by Tamil or English keyword; bilingual detail pages with eligibility, exclusions, documents, steps, benefit and official links.
- Rule-based assistant (`POST /ask`) answering five question types in both languages; safe fallback for unknown questions.
- Last-verified date (18 Nov 2026) and caveat on every page; official-domain allowlist tested in code.
- Mobile-friendly CSS, keyboard focus states, no analytics, no storage of questions.

## Endpoints

| Route | Purpose |
|---|---|
| `/` | Home, search and assistant (`?q=` and `?lang=ta|en`) |
| `/scheme/<id>` | Scheme detail page |
| `/sources` | Official source register |
| `/ask` | POST JSON `{"q": "...", "lang": "ta|en"}` → answer JSON |
| `/api/schemes` | JSON list of schemes |
| `/healthz` | Health check |

## Project structure

```
scheme_sathi/
  app.py                         Flask app + search/intent logic
  data/schemes.json              Bilingual verified scheme content
  templates/                     base, home, scheme, sources, 404
  static/style.css               Responsive, accessible styling
  tests/test_app.py              16 unit/integration tests
  docs/PROBLEM_ANALYSIS.md       All 20 booklet statements filtered
  docs/SOURCE_VERIFICATION.md    12 official sources checked today
  docs/USER_TESTING_NOTES.md     Validation + honest limitations
  docs/IMPLEMENTATION_PLAN_AND_COST.md
  docs/PITCH_DECK.md             10-slide pitch outline
  requirements.txt
```

## Safety

This is an information guide, not an eligibility decision or application service. Final eligibility is decided by the relevant government department. Do not enter Aadhaar, ration-card or bank details anywhere in this prototype. Re-verify scheme data quarterly and after official notifications.
