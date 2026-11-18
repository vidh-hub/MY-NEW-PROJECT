# Implementation plan, cost and risks — AI02

## Work packages completed today (18 Nov 2026)

| # | Work package | Output | Status |
|---|---|---|---|
| 1 | Analyse all 20 booklet problems; filter hardware work | `docs/PROBLEM_ANALYSIS.md` | Done |
| 2 | Research official scheme sources | `docs/SOURCE_VERIFICATION.md` | Done |
| 3 | Model 5 schemes bilingually | `data/schemes.json` | Done |
| 4 | Build searchable FAQ + rule-based assistant | `app.py`, `templates/`, `static/style.css` | Done |
| 5 | Add safety caveats, last-verified dates, official links | App UI + data | Done |
| 6 | Test and validate | `tests/test_app.py` (16 tests) + live smoke test | Done |
| 7 | Document testing, limitations, pitch | `USER_TESTING_NOTES.md`, `PITCH_DECK.md`, `README.md` | Done |

## Cost estimate

| Item | Cost | Notes |
|---|---|---|
| Development laptop, Python 3.13, Flask, VS Code | ₹0 | Already available on this machine |
| Domain / hosting for local demo | ₹0 | Runs on `127.0.0.1:5000` |
| Optional low-cost cloud VM for public pilot | ~₹150–₹300/month | Only if a pilot is requested |
| Optional domain name | ~₹0–₹600/year | Free/low-cost registrars; `.gov.in` not applicable |
| Data verification effort | ~1–2 hours/quarter | Manual re-check of 12 official links |
| Hardware | ₹0 | No sensors, devices or lab needed |

**Prototype build cost today: ₹0.**

## Target users and market

- Primary: rural women and self-help-group (SHG) members in Tamil Nadu who cannot easily navigate English-heavy portals.
- Secondary: SHG facilitators, CSC operators and panchayat volunteers who guide applicants.
- Demand signal: the four districts named in the booklet (Hosur/Krishnagiri, Vellore, Tirupathur) have large SHG and small-farmer populations; scheme information is scattered across many portals.

## Risks and mitigations

| Risk | Mitigation in this prototype |
|---|---|
| Scheme rules change after verification | `last_verified` date on every page; official links; quarterly re-verification plan |
| User thinks eligibility check is final approval | Prominent caveat: "final decision by officials"; no eligibility verdict, only information |
| Misuse for collecting personal data | No personal-data fields; no storage; privacy note in footer |
| Tamil terminology unclear to first-time users | Plain-language phrasing; English toggle; limits documented for field testing |
| Assistant misreads a question | Rule-based intent scoring; safe "no scheme matched" fallback instead of a guess |
| Digital divide / no smartphone | Mobile-friendly layout; designed for assisted use at SHG/CSC; offline use is a future enhancement |
| Flask dev server used in production | Documented as demo-only; use WSGI server for a public deployment |

## Execution milestones (next 4 weeks, if continued)

1. Week 1: field comprehension test with 5–8 SHG members; fix Tamil wording.
2. Week 2: add 5 more frequently asked schemes (e.g., health, housing, work) from official sources.
3. Week 3: add anonymous feedback + CSC-assisted flow; accessibility review with screen reader.
4. Week 4: deploy behind a WSGI server, publish source-verification calendar, hand over to programme mentors.
