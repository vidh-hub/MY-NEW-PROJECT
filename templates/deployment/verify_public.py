"""Verify a deployed Scheme Sathi URL from any machine.

Usage: py deployment/verify_public.py https://<your-site>.pythonanywhere.com
"""

from __future__ import annotations

import json
import sys
from urllib.parse import urlparse

import requests

CHECKS = [
    ("GET /healthz", "/healthz", None),
    ("GET / (Tamil home)", "/", None),
    ("GET /?lang=en (English home)", "/?lang=en", None),
    ("GET /scheme/kmut (scheme detail)", "/scheme/kmut", None),
    ("GET /sources (source register)", "/sources", None),
    ("GET /api/schemes", "/api/schemes", None),
]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base = sys.argv[1].rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme != "https":
        print("WARNING: link is not HTTPS.")

    failures = []
    for label, path, _ in CHECKS:
        try:
            response = requests.get(base + path, timeout=30)
            ok = response.status_code == 200
            print(f"{'PASS' if ok else 'FAIL'}  {label}: HTTP {response.status_code}")
            if not ok:
                failures.append(label)
        except requests.RequestException as exc:
            print(f"FAIL  {label}: {exc}")
            failures.append(label)

    try:
        response = requests.post(
            base + "/ask",
            json={"q": "கலைஞர் திட்டத்திற்கு என்ன ஆவணங்கள்?", "lang": "ta"},
            timeout=30,
        )
        data = response.json()
        ok = response.status_code == 200 and data.get("scheme_id") == "kmut" and len(data.get("bullets", [])) >= 3
        print(f"{'PASS' if ok else 'FAIL'}  POST /ask (Tamil answer): HTTP {response.status_code}")
        if not ok:
            failures.append("POST /ask")
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"FAIL  POST /ask: {exc}")
        failures.append("POST /ask")

    print("\nDeployment verified." if not failures else f"\nFailures: {', '.join(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
