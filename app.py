"""AI02 - Multilingual Government Scheme Assistant (Scheme Sathi).

Tamil-first, software-only prototype for STARTUP TN24 problem statement AI02.
No hardware, no personal data collection, no external services required.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "schemes.json"

with DATA_FILE.open(encoding="utf-8") as fh:
    SCHEMES = json.load(fh)

BY_ID = {scheme["id"]: scheme for scheme in SCHEMES}
VERIFIED_DATE = "2026-11-18"

OFFICIAL_DOMAINS = {
    "kmut.tn.gov.in",
    "pmkisan.gov.in",
    "financialservices.gov.in",
    "pib.gov.in",
    "rbi.org.in",
    "indiapost.gov.in",
    "india.gov.in",
    "jansamarth.in",
    "www.indiapost.gov.in",
    "www.pib.gov.in",
    "www.rbi.org.in",
    "www.india.gov.in",
    "www.jansamarth.in",
}

LABELS = {
    "ta": {
        "app_name": "திட்டத் தோழி",
        "app_sub": "அரசு திட்டங்களை எளிய தமிழில் புரிந்து கொள்ளுங்கள்",
        "nav_home": "முகப்பு",
        "nav_sources": "அதிகாரப்பூர்வ மூலங்கள்",
        "hero_title": "உங்களுக்கான அரசு திட்டம் — எளிய தமிழில்",
        "hero_text": "தகுதி, தேவையான ஆவணங்கள், விண்ணப்பிக்கும் வழி மற்றும் அதிகாரப்பூர்வ இணையதளம் — அனைத்தும் ஒரே இடத்தில். நாங்கள் விண்ணப்பங்களைப் பெறுவதில்லை; தகவல் மட்டுமே தருகிறோம்.",
        "search_label": "திட்டம் தேடுங்கள் (தமிழ் அல்லது ஆங்கிலம்)",
        "search_button": "தேடு",
        "all_schemes": "அனைத்து திட்டங்கள்",
        "results_for": "தேடல் முடிவுகள்",
        "no_results": "இந்தத் தேடலுக்கு திட்டம் கிடைக்கவில்லை. 'கலைஞர்', 'கிசான்', 'முத்ரா', 'SHG', 'சுகன்யா' ஆகிய சொற்களைப் பயன்படுத்திப் பார்க்கவும்.",
        "assistant_title": "கேள்வி கேளுங்கள்",
        "assistant_text": "எடுத்துக்காட்டு: \"கலைஞர் திட்டத்திற்கு என்ன ஆவணங்கள் வேண்டும்?\" அல்லது \"PM Kisan eligibility\"",
        "ask_button": "பதில் காண்க",
        "details": "விவரங்கள் காண்க",
        "verified": "அதிகாரப்பூர்வ மூலங்களுடன் சரிபார்க்கப்பட்டது",
        "disclaimer": "இது தகவல் வழிகாட்டி மட்டுமே. இறுதி தகுதி மற்றும் தொகைக்கு அதிகாரப்பூர்வ இணையதளம் அல்லது உள்ளூர் அலுவலகத்தை அணுகவும். ஆதார் எண், குடும்ப அட்டை, வங்கி விவரங்களை இங்கே உள்ளிட வேண்டாம்.",
        "privacy": "தனியுரிமை: இந்த முன்மாதிரி உங்கள் கேள்விகளைச் சேமிக்கவோ, கண்காணிக்கவோ, மூன்றாம் தரப்பிற்கு அனுப்பவோ இல்லை.",
        "question": "கேள்வி",
        "answer": "பதில்",
        "official_source": "அதிகாரப்பூர்வ மூலம்",
        "sources_title": "அதிகாரப்பூர்வ மூலங்கள்",
        "sources_text": "ஒவ்வொரு திட்டத்தின் தகவலும் பின்வரும் அரசு இணையதளங்களிலிருந்து எடுக்கப்பட்டு 18.11.2026 அன்று சரிபார்க்கப்பட்டது. புதிய அறிவிப்புகளை மீண்டும் பார்க்கவும்.",
        "back_home": "முகப்பிற்கு மீண்டும் செல்லுங்கள்",
        "benefit": "பலன்",
        "who": "யார் தகுதியுடையவர்?",
        "eligibility": "தகுதி நிபந்தனைகள்",
        "exclusions": "தகுதி இல்லாதவர்கள்",
        "documents": "தேவையான ஆவணங்கள்",
        "how_to_apply": "விண்ணப்பிக்கும் முறை",
        "apply_official": "அதிகாரப்பூர்வமாக விண்ணப்பிக்க / நிலை பார்க்க",
        "last_verified": "கடைசியாக சரிபார்க்கப்பட்டது",
        "try_again": "மற்றொரு கேள்வி கேளுங்கள்",
        "loading": "பதில் தயாராகிறது...",
    },
    "en": {
        "app_name": "Scheme Sathi",
        "app_sub": "Understand government schemes in plain language",
        "nav_home": "Home",
        "nav_sources": "Official sources",
        "hero_title": "Government schemes, explained simply",
        "hero_text": "Eligibility, documents, application steps and official links — all in one place. We do not accept applications; we only provide guidance.",
        "search_label": "Search a scheme (Tamil or English)",
        "search_button": "Search",
        "all_schemes": "All schemes",
        "results_for": "Search results",
        "no_results": "No scheme matched. Try: Kalaignar, PM Kisan, MUDRA, SHG or Sukanya.",
        "assistant_title": "Ask a question",
        "assistant_text": "Example: \"What documents are needed for Kalaignar Urimai?\" or \"PM Kisan eligibility\"",
        "ask_button": "Get answer",
        "details": "View details",
        "verified": "Checked against official sources",
        "disclaimer": "This is an information guide only. Final eligibility and amounts are decided by official portals or your local office. Do not enter Aadhaar, ration-card or bank details here.",
        "privacy": "Privacy: this prototype does not store, track or forward your questions to third parties.",
        "question": "Question",
        "answer": "Answer",
        "official_source": "Official source",
        "sources_title": "Official sources",
        "sources_text": "Every scheme note was checked against the government websites below on 18 November 2026. Re-check for new notices before applying.",
        "back_home": "Back to home",
        "benefit": "Benefit",
        "who": "Who can apply",
        "eligibility": "Eligibility conditions",
        "exclusions": "Who is not eligible",
        "documents": "Documents needed",
        "how_to_apply": "How to apply",
        "apply_official": "Apply / check status on the official site",
        "last_verified": "Last verified",
        "try_again": "Ask another question",
        "loading": "Preparing answer...",
    },
}

TOPIC_LABELS = {
    "ta": {
        "overview": "சுருக்கமான தகவல்",
        "benefit": "பலன்",
        "eligibility": "தகுதி நிபந்தனைகள்",
        "exclusions": "தகுதி இல்லாதவர்கள்",
        "documents": "தேவையான ஆவணங்கள்",
        "apply": "விண்ணப்பிக்கும் முறை",
    },
    "en": {
        "overview": "Overview",
        "benefit": "Benefit",
        "eligibility": "Eligibility conditions",
        "exclusions": "Who is not eligible",
        "documents": "Documents needed",
        "apply": "How to apply",
    },
}

# Specific hints score higher than generic ones so "SHG loan" resolves to the
# SHG scheme rather than the generic word "loan" in the MUDRA scheme.
SCHEME_HINTS = {
    "kmut": [
        (r"கலைஞர்", 3), (r"உரிமை", 3), (r"kmut", 3), (r"urimai", 3),
        (r"kalaignar", 3), (r"மகளிர்", 2), (r"ration card", 2), (r"குடும்ப அட்டை", 2),
    ],
    "pmkisan": [
        (r"கிசான்", 3), (r"pm.?kisan", 3), (r"விவசாய", 2), (r"farmer", 2),
        (r"நிலம்", 1), (r"\bland\b", 1), (r"patta", 1),
    ],
    "pmmy": [
        (r"முத்ரா", 3), (r"mudra", 3), (r"pmmy", 3), (r"தொழில்", 2),
        (r"business", 2), (r"enterprise", 2), (r"கடன்", 1), (r"\bloan\b", 1),
    ],
    "daynrlm": [
        (r"\bshg\b", 3), (r"சுய.?உதவி", 3), (r"nrlm", 3), (r"சுழல்நிதி", 3),
        (r"revolving", 3), (r"குழு", 2), (r"\bgroup\b", 2),
    ],
    "ssy": [
        (r"சுகன்யா", 3), (r"sukanya", 3), (r"\bssy\b", 3), (r"மகள்", 2),
        (r"\bgirl\b", 2), (r"சேமிப்பு", 2), (r"savings", 2),
    ],
}

TOPIC_HINTS = [
    ("documents", [(r"ஆவண", 3), (r"சான்று", 2), (r"\bdocuments?\b", 3), (r"\bdoc\b", 2), (r"தேவையான", 1)]),
    ("apply", [(r"விண்ணப்ப", 3), (r"எப்படி", 2), (r"\bapply\b", 3), (r"\bapplication\b", 3), (r"how to", 2), (r"csc", 2), (r"முகாம்", 2)]),
    ("eligibility", [(r"தகுதி", 3), (r"eligib", 2), (r"who can", 2), (r"யார்", 1)]),
    ("exclusions", [(r"தகுதி இல்ல", 6), (r"exclu", 5), (r"not eligible", 5), (r"விலக்க", 4)]),
    ("benefit", [(r"பலன்", 3), (r"தொகை", 2), (r"\bbenefit\b", 3), (r"எவ்வளவு", 2), (r"how much", 2), (r"₹", 1)]),
]

app = Flask(__name__)


def current_lang() -> str:
    return "en" if request.args.get("lang") == "en" or request.form.get("lang") == "en" else "ta"


def t(scheme: dict, name: str, lang: str):
    return scheme.get(f"{name}_{lang}", "")


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def detect_scheme(query: str) -> str | None:
    text = norm(query)
    scores = {}
    for sid, hints in SCHEME_HINTS.items():
        score = sum(weight for pattern, weight in hints if re.search(pattern, text, re.I))
        if score:
            scores[sid] = score
    if not scores:
        return None
    # Deterministic tie-break: booklet order.
    return max(scores, key=lambda sid: (scores[sid], -list(BY_ID).index(sid)))


def detect_topic(query: str) -> str:
    text = norm(query)
    scores = {}
    for topic, hints in TOPIC_HINTS:
        score = sum(weight for pattern, weight in hints if re.search(pattern, text, re.I))
        if score:
            scores[topic] = score
    if not scores:
        return "overview"
    return max(scores, key=lambda topic: (scores[topic], -[x[0] for x in TOPIC_HINTS].index(topic)))


def search_schemes(query: str) -> list[dict]:
    q = norm(query)
    if not q:
        return list(SCHEMES)
    stopwords = {"the", "for", "and", "not", "scheme", "திட்டம்", "என்ன"}
    tokens = [
        tok for tok in re.split(r"[\s,?|-]+", q)
        if len(tok) >= 3 and tok not in stopwords
    ]
    ranked = []
    for scheme in SCHEMES:
        name = norm(f"{t(scheme, 'name', 'ta')} {t(scheme, 'name', 'en')}")
        keywords = norm(" ".join(t(scheme, "keywords", "ta") + t(scheme, "keywords", "en")))
        body = norm(" ".join(t(scheme, "who", "ta") + t(scheme, "who", "en") + t(scheme, "tagline", "ta") + t(scheme, "tagline", "en")))
        score = 0
        if q in name:
            score += 8
        for token in tokens:
            if token in name:
                score += 4
            if token in keywords:
                score += 3
            if token in body:
                score += 1
        if score >= 2:
            ranked.append((score, scheme))
    ranked.sort(key=lambda item: (-item[0], list(BY_ID).index(item[1]["id"])))
    return [scheme for _, scheme in ranked]


def build_answer(query: str, lang: str) -> dict:
    sid = detect_scheme(query)
    if not sid:
        return {
            "scheme_id": None,
            "title": LABELS[lang]["try_again"],
            "bullets": [],
            "caveat": LABELS[lang]["disclaimer"],
            "sources": [],
            "official_url": None,
            "text": LABELS[lang]["no_results"],
        }

    scheme = BY_ID[sid]
    topic = detect_topic(query)
    title = f"{t(scheme, 'name', lang)} — {TOPIC_LABELS[lang][topic]}"

    if topic == "overview":
        bullets = (
            [t(scheme, "benefit", lang)[0]] if t(scheme, "benefit", lang) else []
        ) + t(scheme, "who", lang).split("\n")
    else:
        bullets = list(t(scheme, topic, lang))

    sources = [f"{src['title']}: {src['url']}" for src in scheme["official_sources"]]
    text_lines = [title] + [f"- {b}" for b in bullets]
    text_lines += [t(scheme, "caveat", lang), f"{LABELS[lang]['official_source']}: {scheme['apply_url']}"]
    text_lines += sources

    return {
        "scheme_id": sid,
        "title": title,
        "bullets": bullets,
        "caveat": t(scheme, "caveat", lang),
        "sources": sources,
        "official_url": scheme["apply_url"],
        "text": "\n".join(text_lines),
    }


@app.context_processor
def inject_common():
    lang = current_lang()
    return {
        "lang": lang,
        "labels": LABELS[lang],
        "verified_date": VERIFIED_DATE,
        "schemes": SCHEMES,
    }


@app.get("/")
def home():
    query = request.args.get("q", "")
    return render_template(
        "home.html",
        results=search_schemes(query),
        query=query,
    )


@app.get("/scheme/<sid>")
def scheme_detail(sid):
    if sid not in BY_ID:
        abort(404)
    return render_template("scheme.html", scheme=BY_ID[sid])


@app.get("/sources")
def sources():
    return render_template("sources.html")


@app.post("/ask")
def ask():
    payload = request.get_json(silent=True) or request.form
    query = str(payload.get("q", ""))
    lang = "en" if str(payload.get("lang", "ta")) == "en" else "ta"
    return jsonify(build_answer(query, lang))


@app.get("/api/schemes")
def api_schemes():
    lang = current_lang()
    return jsonify([
        {
            "id": s["id"],
            "name": t(s, "name", lang),
            "tagline": t(s, "tagline", lang),
            "apply_url": s["apply_url"],
            "verified": s["last_verified"],
        }
        for s in SCHEMES
    ])


@app.get("/healthz")
def healthz():
    return "ok", 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("not_found.html"), 404


def all_source_urls() -> list[str]:
    return [src["url"] for s in SCHEMES for src in s["official_sources"]] + [s["apply_url"] for s in SCHEMES]


def sources_are_official() -> bool:
    return all(urlparse(url).hostname in OFFICIAL_DOMAINS for url in all_source_urls())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
