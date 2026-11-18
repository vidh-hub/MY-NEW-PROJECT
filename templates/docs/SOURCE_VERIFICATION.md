# Official source verification register — AI02

All scheme content was checked on **18 November 2026** against government websites. The app displays these links and the same last-verified date on every scheme page.

| Scheme | Official source | Key facts verified | Page status / note |
|---|---|---|---|
| Kalaignar Magalir Urimai Thogai (TN) | https://kmut.tn.gov.in/about-kmut.html | Eligibility: family income < ₹2.5 lakh; < 5 acres irrigated / < 10 acres rainfed land; < 3,600 electricity units/year; woman beneficiary aged 21+; one per ration card. Benefit ₹1,000/month. Exclusions listed. | Official TN government site |
| Kalaignar Magalir Urimai Thogai (TN) | https://kmut.tn.gov.in/faq.html | Apply at camp linked to fair-price shop / e-Sevai centre; status via Aadhaar login; appeal within 30 days of rejection SMS; ration card + Aadhaar-linked bank account required. | Official FAQ |
| Kalaignar Magalir Urimai Thogai (TN) | https://kmut.tn.gov.in/login.html | Official status-check/login route (we only link; we never ask for Aadhaar). | Official portal |
| PM Kisan Samman Nidhi | https://pmkisan.gov.in/ | ₹6,000/year in 3 instalments; family = husband, wife, minor children; land records; eKYC mandatory; 01.02.2019 cut-off; exclusion categories; KYS status check. | Portal shows "Page Last Updated on: 20/06/2025"; 23rd instalment released 20 June 2026 |
| PM Kisan Samman Nidhi | https://pmkisan.gov.in/Documents/RevisedPM-KISANOperationalGuidelines(English).pdf | Operational guidelines: benefit, family definition, exclusions, eligibility calculation, 01.02.2019 cut-off. | Official PDF |
| PM Kisan Samman Nidhi | https://pmkisan.gov.in/Documents/RevisedFAQ.pdf | No 2-hectare limit after 01.06.2019; all landholding families covered. | Official PDF |
| Pradhan Mantri MUDRA Yojana | https://financialservices.gov.in/pradhan-mantri-mudra-yojana-pmmy | Collateral-free credit; Shishu ≤ ₹50,000; Kishor ₹50,001–₹5 lakh; Tarun ₹5–10 lakh; Tarun Plus ₹10–20 lakh; agriculture-allied activities included; MLIs listed. | Department of Financial Services, GoI |
| Pradhan Mantri MUDRA Yojana | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2240159 | 14 March 2026 PIB release confirming categories, collateral-free loans up to ₹20 lakh and Jan Samarth application route. | Official PIB |
| DAY-NRLM SHG | https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=12806 | RBI Master Circular dated 1 April 2025: women SHGs of 10–20 (min 5 special), ₹20,000–₹30,000 revolving fund, Panchasutras, 6-month rule, ₹1 lakh MUDRA loan per SHG member, ₹10 lakh individual loans for mature SHGs, ₹5,000 minimum OD for PMJDY members, wilful defaulters excluded. | Official RBI |
| Sukanya Samriddhi Yojana | https://www.indiapost.gov.in/banking-services/saving | Small savings scheme; notified interest rate 8.2% at time of check; account-opening documents; birth certificate mandatory. | Official India Post |
| Sukanya Samriddhi Yojana | https://www.pib.gov.in/PressNoteDetails.aspx?NoteId=157019 | 21 Jan 2026 explainer: girl child below 10, one account per child (max two families, twins/triplets exception), documents (form, birth certificate, Aadhaar, PAN/Form 60), ₹250 minimum, ₹1.5 lakh annual cap, 50% withdrawal at 18, transferable. | Official PIB |
| Sukanya Samriddhi Yojana | https://www.india.gov.in/sukanya-samriddhi-yojna | National Portal reference page. | Official GoI portal |

## Verification rules used in the app

- Every displayed scheme has at least one official source link.
- Every scheme shows `last_verified = 2026-11-18`.
- All source domains are restricted to an allowlist of government domains (`kmut.tn.gov.in`, `pmkisan.gov.in`, `financialservices.gov.in`, `pib.gov.in`, `rbi.org.in`, `indiapost.gov.in`, `india.gov.in`, `jansamarth.in`) — enforced by an automated test.
- Interest rates, eligibility cut-offs and scheme rules can change. The app keeps a plain-language caveat on every answer and detail page and sends users to the official portal for the final decision.

## Maintenance

Re-verify all 12 sources and update `data/schemes.json` + `VERIFIED_DATE` in `app.py` **at least once every quarter**, and immediately after a Union/State budget or scheme notification.
