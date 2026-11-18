# Final pitch deck outline — AI02 / Scheme Sathi

10 slides, following the booklet's "Final Pitch Deck & Review Checklist" (page 18).

## 1. Cover / Introduction
**Scheme Sathi — Multilingual Government Scheme Assistant**
STARTUP TN24 · AI02 · Team: [team name] · 18 Nov 2026

## 2. Problem Statement
Rural women and SHG members in Tamil Nadu struggle to find and apply for government schemes: portals are English-heavy, eligibility is written in official language, and information is scattered. They often rely on intermediaries and miss benefits.
Evidence: official scheme pages reviewed; four-district focus from the programme booklet; no field survey claimed today (see limitations).

## 3. Existing Solutions
- Individual scheme portals (KMUT, PM-Kisan, Jan Samarth, India Post) — accurate but fragmented and formal in tone.
- myScheme / aggregator portals — broad coverage, still complex for first-time users.
- Helpers/CSC/SHG workers — trusted but overloaded.
**Gap:** one plain-language, Tamil-first, verified starting point that explains and then hands off to official channels.

## 4. Your Solution
- Tamil-first web assistant with English toggle.
- Five verified schemes: KMUT, PM-Kisan, PM MUDRA, DAY-NRLM SHGs, Sukanya Samriddhi.
- Search + full detail pages + question answering (eligibility, documents, how to apply, benefit, exclusions).
- Every answer shows source links, last-verified date and a safety caveat.
- No applications, no personal data.

## 5. Prototype / PoC
Live Flask web app; 16 automated tests passing; 6 HTTP endpoints smoke-tested; `/ask` answers in Tamil and English. Demo flow: search "கலைஞர்" → detail page → ask "என்ன ஆவணங்கள்?" → official portal link.

## 6. Unique Selling Proposition
- Verified against official government domains, not scraped rumour.
- Plain Tamil with eligibility caveats instead of a yes/no verdict.
- Direct hand-off to the correct official application channel.
- Privacy-first: nothing is collected; works on a basic phone browser.

## 7. Market Opportunity
Target users: rural women, SHG members and their facilitators in Hosur, Krishnagiri, Vellore and Tirupathur; scalable to all of Tamil Nadu and other Indian languages. Alternatives are fragmented portals and paid/unofficial middlemen.

## 8. Revenue Model (if scaled)
- Free for citizens; optional SaaS/AMC for SHG federations, CSC networks and NGOs to host a co-branded instance.
- Content-verification service for local bodies.
- Zero marginal cost per additional user; no transaction fees on benefits.

## 9. Execution Plan
Built today: research → data model → app → tests → documentation.
Next: field comprehension testing (week 1), 5 more schemes (week 2), assisted/CSC flow + accessibility (week 3), WSGI deployment + verification calendar (week 4). Roles: content lead, Flask developer, field researcher, reviewer.

## 10. Traction / Validation
16/16 automated tests pass; live demo works in both languages; official-domain check enforced in code; scripted 5-task walkthrough passed; limitations documented (no external user test yet). Prototype build cost: ₹0.
