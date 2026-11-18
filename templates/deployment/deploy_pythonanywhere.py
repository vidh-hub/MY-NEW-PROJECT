"""Deploy Scheme Sathi to PythonAnywhere and verify the public HTTPS URL.

Run from this folder:
    py deployment/deploy_pythonanywhere.py

You need a free PythonAnywhere account and its API token:
    Account page -> "API Token" tab -> "Create a new API token".

Credentials can also be supplied via environment variables:
    PYTHONANYWHERE_USERNAME, PYTHONANYWHERE_TOKEN, PYTHONANYWHERE_REGION (www|eu)

Uses only the Python standard library + requests (already installed).
"""

from __future__ import annotations

import getpass
import os
import pathlib
import sys
import time

import requests

LOCAL_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {"__pycache__", "deployment", ".git", ".pytest_cache", ".venv"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
REQUEST_TIMEOUT = 60


def api_url(host: str, username: str, tail: str) -> str:
    return f"https://{host}.pythonanywhere.com/api/v0/user/{username}/{tail}"


def headers(token: str) -> dict:
    return {"Authorization": f"Token {token}"}


def check(response: requests.Response, action: str) -> requests.Response:
    if response.status_code not in (200, 201, 204):
        raise RuntimeError(
            f"{action} failed: HTTP {response.status_code}\n{response.text[:800]}"
        )
    return response


def create_webapp(host: str, username: str, token: str, domain: str) -> str:
    url = api_url(host, username, "webapps/")
    existing = check(
        requests.get(url, headers=headers(token), timeout=REQUEST_TIMEOUT),
        "Listing existing webapps",
    ).json()
    domains = [site["domain_name"] for site in existing]
    if domain in domains:
        print(f"  Webapp {domain} already exists - reusing it.")
        return "existing"

    # PythonAnywhere has used several version strings over time; try the
    # current ones in order until one is accepted.
    for version in ("3.12", "python312", "3.11", "python311", "3.10", "python310"):
        response = requests.post(
            url,
            data={"domain_name": domain, "python_version": version},
            headers=headers(token),
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code in (200, 201):
            print(f"  Created webapp with python_version={version}")
            return version
        print(f"  python_version={version} rejected (HTTP {response.status_code}); trying next")
    raise RuntimeError("Could not create webapp with any supported Python version.")


def upload_file(host: str, username: str, token: str, remote_path: str, data: bytes, name: str) -> None:
    url = api_url(host, username, f"files/path{remote_path}")
    check(
        requests.post(
            url,
            files={"content": (name, data)},
            headers=headers(token),
            timeout=REQUEST_TIMEOUT,
        ),
        f"Uploading {remote_path}",
    )


def upload_project(host: str, username: str, token: str, project_home: str) -> int:
    count = 0
    for local in sorted(LOCAL_ROOT.rglob("*")):
        if not local.is_file():
            continue
        rel = local.relative_to(LOCAL_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts) or local.suffix in SKIP_SUFFIXES:
            continue
        remote = f"{project_home}/{rel.as_posix()}"
        upload_file(host, username, token, remote, local.read_bytes(), local.name)
        count += 1
    return count


def configure_static(host: str, username: str, token: str, domain: str, project_home: str) -> None:
    url = api_url(host, username, f"webapps/{domain}/static_files/")
    current = check(
        requests.get(url, headers=headers(token), timeout=REQUEST_TIMEOUT),
        "Reading static file mappings",
    ).json()
    urls = [item["url"] for item in current]
    for url_path in ("/static", "/static/"):
        if url_path in urls:
            print(f"  Static mapping {url_path} already present")
            return
    check(
        requests.post(
            url,
            data={"url": "/static", "path": f"{project_home}/static"},
            headers=headers(token),
            timeout=REQUEST_TIMEOUT,
        ),
        "Creating /static mapping",
    )
    print("  Created /static mapping")


def verify(domain: str) -> str:
    last_error = ""
    for scheme in ("https", "http"):
        base = f"{scheme}://{domain}"
        try:
            health = requests.get(f"{base}/healthz", timeout=30)
            home = requests.get(base, timeout=30)
            if health.status_code == 200 and home.status_code == 200 and "AI02" in home.text:
                return base
            last_error = f"health={health.status_code}, home={home.status_code}"
        except requests.RequestException as exc:
            last_error = str(exc)
    raise RuntimeError(f"Public verification failed ({last_error}). Check the webapp error log.")


def main() -> int:
    host = os.environ.get("PYTHONANYWHERE_REGION", "").strip().lower() or input(
        "Region (www for pythonanywhere.com, eu for eu.pythonanywhere.com) [www]: "
    ).strip().lower() or "www"
    if host not in ("www", "eu"):
        print("Region must be 'www' or 'eu'.")
        return 2

    username = os.environ.get("PYTHONANYWHERE_USERNAME", "").strip() or input(
        "PythonAnywhere username: "
    ).strip()
    token = os.environ.get("PYTHONANYWHERE_TOKEN", "").strip() or getpass.getpass(
        "PythonAnywhere API token (input hidden): "
    ).strip()
    if not username or not token:
        print("Username and API token are required.")
        return 2

    domain = f"{username}.pythonanywhere.com" if host == "www" else f"{username}.eu.pythonanywhere.com"
    project_home = f"/home/{username}/scheme_sathi"
    wsgi_remote = f"/var/www/{domain.replace('.', '_')}_wsgi.py"
    wsgi_content = (
        "import sys\n\n"
        f"project_home = {project_home!r}\n"
        "if project_home not in sys.path:\n"
        "    sys.path.insert(0, project_home)\n\n"
        "from app import app as application  # noqa: E402\n"
    )

    print(f"\nTarget: https://{domain}/")
    print("Step 1/5: creating or reusing the webapp")
    create_webapp(host, username, token, domain)

    print(f"Step 2/5: uploading project files to {project_home}")
    count = upload_project(host, username, token, project_home)
    print(f"  Uploaded {count} files")

    print("Step 3/5: writing the WSGI entry point")
    upload_file(host, username, token, wsgi_remote, wsgi_content.encode("utf-8"), "wsgi.py")

    print("Step 4/5: configuring static files and reloading")
    configure_static(host, username, token, domain, project_home)
    check(
        requests.post(
            api_url(host, username, f"webapps/{domain}/reload/"),
            headers=headers(token),
            timeout=REQUEST_TIMEOUT,
        ),
        "Reloading webapp",
    )
    print("  Webapp reloaded")

    print("Step 5/5: waiting for the site and verifying it")
    public_base = ""
    for attempt in range(10):
        try:
            public_base = verify(domain)
            break
        except RuntimeError as exc:
            if attempt == 9:
                print(f"  Verification error: {exc}")
                break
            time.sleep(3)
    if not public_base:
        print("\nDeployment uploaded but verification failed. Check the error log in the PythonAnywhere Web tab.")
        return 1

    print(f"\nSUCCESS: {public_base}/")
    print("Share this link on WhatsApp / email / LinkedIn.")
    print("It stays online when your computer is switched off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
