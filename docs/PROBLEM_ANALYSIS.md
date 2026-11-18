# STARTUP TN24 — Analysis of all 20 problem statements

Source: `STARTUP_TN24_Problem_Statement_Booklet.pdf` (18 pages, 20 briefs).

## Filter result

| ID | Problem | Hardware / physical dependency? | Software-only today? | Decision |
|---|---|---|---|---|
| AG01 | Smart Polyhouse Monitoring | Yes — sensors, controllers | No | Excluded |
| AG02 | AI Crop Pest & Disease Support | No hardware (images only) | Conditional — needs credible labelled crop-image dataset and expert validation | Not selected (data risk) |
| AG03 | Wildlife Movement Early Warning | Yes — sensors/camera at farm edge | No | Excluded |
| AG04 | Farmer Direct Market & Price Visibility | No | Yes | Runner-up (needs farmer/buyer interviews for credible research) |
| AG05 | Smart Irrigation & Water Data | Yes — soil-moisture/water-level sensors | No (dashboard alone is not the problem) | Excluded |
| AI01 | AI Visual Quality Inspector | No hardware (images only) | Conditional — needs a permitted labelled defect dataset | Not selected (data risk) |
| AI02 | Multilingual Government Scheme Assistant | **No** | **Yes** | **Selected and implemented** |
| AI03 | Industrial PPE & Safety Monitor | Yes — camera/sensor footage | No | Excluded |
| AI04 | Predictive Maintenance for MSMEs | Yes — vibration/temperature/current sensors | No | Excluded |
| AI05 | Assistive Vision & Text Recognition | Yes — mobile/embedded device with camera/audio | No | Excluded |
| FT01 | Mango & Tomato Value Addition | Yes — food processing equipment, lab | No | Excluded |
| FT02 | Millet Product Innovation | Yes — product batches, shelf-life lab | No | Excluded |
| FT03 | Affordable Food Quality Screening | Yes — test kits/reagents | No | Excluded |
| FT04 | Agro-Waste Biodegradable Packaging | Yes — material processing | No | Excluded |
| FT05 | Affordable Cold Storage | Yes — insulation, cooling, power backup | No | Excluded |
| BT01 | Rural Health Screening Access | No (service/booking workflow) | Yes | Runner-up (requires consent-based field conversations) |
| BT02 | Groundwater Quality Monitoring | Yes — sensors + accredited lab confirmation | No | Excluded |
| BT03 | Soil Health & Sustainable Inputs | No (data format only) | Conditional — needs qualified agronomy guidance/sample records | Not selected |
| BT04 | Flower Waste to Value-Added Products | Yes — collection and conversion | No | Excluded |
| BT05 | Tannery Effluent Monitoring & Treatment | Yes — chemical testing/lab supervision | No | Excluded |

## Software-only shortlist

1. **AI02 — Multilingual Government Scheme Assistant**
2. AG04 — Farmer Direct Market & Price Visibility
3. BT01 — Rural Health Screening Access
4. BT03 — Soil Health & Sustainable Inputs (data workflow only)
5. AG02 / AI01 — only if a reliable labelled image dataset is already available

## Why AI02 was selected

- **Zero hardware**: no sensors, devices, cameras or lab access needed.
- **All required deliverables can be produced today**: official-source verification, Tamil-first user journeys, searchable FAQ + rule-based assistant, eligibility caveats, source links with last-verified dates, user-testing notes and safety limitations.
- **Data verified live from official government domains** (KMUT, PM-Kisan, Department of Financial Services/PIB/RBI, India Post/PIB) — no synthetic facts.
- **Fits the brief's safety requirement**: it explains schemes in plain language and routes users to official application channels; it does not collect applications or personal data.
- **Immediate feasibility with available resources**: Python 3.13 + Flask were already installed; no additional packages or hardware were needed.

## What was built

`Scheme Sathi` — a bilingual (Tamil-default, English toggle) Flask web app with:

- 5 verified schemes: KMUT, PM-Kisan, PM MUDRA Yojana, DAY-NRLM women's SHGs, Sukanya Samriddhi Yojana
- search by Tamil/English keywords, full detail pages, official-source register
- rule-based assistant answering "eligibility / documents / apply / benefit / exclusions" questions in both languages
- explicit caveats, last-verified dates, official links, and no personal-data inputs

See `README.md`, `SOURCE_VERIFICATION.md`, `USER_TESTING_NOTES.md`, `IMPLEMENTATION_PLAN_AND_COST.md` and `PITCH_DECK.md`.
