# Testing and validation report — AI02

Date: **18 November 2026**. Prototype: `Scheme Sathi` (Flask web app, Tamil + English).

## 1. Tests executed today

### Automated tests (16/16 passed)

Command: `py -m unittest discover -s tests -v`

Coverage:
- scheme data completeness (bilingual fields, sources, verification date)
- all official-link domains allowlisted
- scheme detection in Tamil and English (5 schemes + unknown query)
- intent detection (documents / eligibility / exclusions / apply / overview)
- keyword search ranking and empty-result handling
- answer content includes caveat + official source and does not invent facts for unknown questions
- web routes: home (Tamil default), English toggle, search filtering, detail page, sources, 404, health check, JSON API
- `/ask` endpoint in both languages
- privacy check: only 3 inputs on the home page (hidden language field, search box, question box) and no password/Aadhaar/account-number fields

### Live HTTP smoke test

App started on `127.0.0.1:5077`; all 6 GET endpoints returned **200** and the `/ask` POST returned a correct KMUT documents answer with 3 bullets.

### Task-based walkthrough (scripted, 5 tasks)

| Task | Query used | Expected result | Actual |
|---|---|---|---|
| Find a women's monthly payment scheme | `கலைஞர்` | KMUT card first | Pass |
| Check PM-Kisan eligibility in English | `PM Kisan eligibility` | PM-Kisan, eligibility bullets | Pass |
| Get documents for MUDRA in Tamil | `முத்ரா கடனுக்கு ஆவணங்கள் என்ன?` | PMMY, documents bullets | Pass |
| Check SHG group support | `SHG கடன்` | DAY-NRLM (not PMMY) | Pass |
| Irrelevant question | `ரசியல் கட்சி பற்றி கூறு` / general English question | No invented answer; "no scheme matched" | Pass |

Manual rendering check: Tamil text renders in the browser with UTF-8, buttons have ≥ 44px touch targets on mobile CSS, colour contrast meets normal text usage, and links open with `rel="noopener noreferrer"`.

## 2. Safety and privacy validation

- No form field collects Aadhaar, ration-card, bank, phone or personal details.
- Questions submitted to `/ask` are processed in memory and not persisted to disk or sent to a third party.
- Every answer and every detail page carries a caveat: final eligibility is decided by officials.
- Every answer links to an official government portal/domain.
- No automated chemical, medical or legal advice is given; the tool only explains publicly available scheme information.

## 3. Limitations (documented honestly)

1. **No external user testing was possible today.** The booklet asks for "test whether users can understand the information"; this was approximated with a scripted task walkthrough and internal review. A real comprehension test with 5–8 rural women / SHG members is still required before field deployment.
2. **Rule-based assistant, not an LLM.** It handles the five included schemes and five question types. Out-of-vocabulary phrasing falls back to "no scheme matched" rather than guessing — intentional for safety.
3. **Five schemes only**, chosen for relevance to rural women and SHG members in Tamil Nadu. More schemes can be added to `data/schemes.json`.
4. **Scheme data is a snapshot** verified on 18 Nov 2026. Interest rates and eligibility rules change; the app displays the verification date and official links.
5. **Digital-access barrier remains**: the target users may need assisted navigation (SHG worker / CSC). The prototype is mobile-friendly but not offline-capable.
6. **Live server warning**: Flask's built-in server is for demonstration only; a production WSGI server is needed for public deployment.

## 4. Suggested next validation round (not done today)

- 5 tasks × 5 participants, think-aloud, measure comprehension of eligibility and where to apply.
- Check Tamil terminology with a local social worker / SHG facilitator.
- Add a feedback button that stores anonymous ratings only (no personal data).
