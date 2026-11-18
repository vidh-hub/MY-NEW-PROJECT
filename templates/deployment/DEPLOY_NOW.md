# Public deployment guide — Scheme Sathi

The app is ready for public hosting. **A hosting account is required**: no hosting credentials, Git account or API token exist on this machine, so I cannot create a public HTTPS URL without one. The recommended option below is free, requires no credit card, gives a permanent `https://<username>.pythonanywhere.com` URL, and stays online when your computer is off.

## Option A (recommended): PythonAnywhere — free HTTPS, permanent

### Step 1 — create the account (2 minutes)
1. Go to <https://www.pythonanywhere.com/registration/register/individual/> (or `eu.pythonanywhere.com` if you prefer EU).
2. Sign up with your email and verify it.
3. In your account, open **Account → API Token → Create a new API token** and copy the token.

### Step 2 — run the prepared deployment script on this machine
```powershell
cd C:\Users\voice\Downloads\STARTUP\scheme_sathi
py deployment\deploy_pythonanywhere.py
```
Enter: username, API token (hidden while typing), and region (`www` or `eu`).

The script will:
- create/reuse the webapp at `https://<username>.pythonanywhere.com`
- upload all application files, templates, static CSS and data
- write the WSGI entry point, map `/static`, reload the server
- verify `/healthz`, the home page and a Tamil `/ask` answer

It ends with `SUCCESS: https://...` — that is your shareable link.

**If you prefer not to share your token in this session:** run the same command yourself in your own terminal, then send me the printed URL and I will verify every feature from here using `py deployment/verify_public.py <URL>`.

### Step 3 — share
Send `https://<username>.pythonanywhere.com` on WhatsApp, email or LinkedIn. It works on mobile and desktop and does not depend on your computer being on.

## Option B: Render (requires a GitHub account)

`deployment/render.yaml` and `Procfile` are included. Push this folder to a GitHub repository, then:
1. Sign in at <https://render.com> with GitHub.
2. **New + → Blueprint** → select the repository → **Apply**.
3. Render builds with `gunicorn`, adds a free HTTPS certificate and provides a `*.onrender.com` URL.

Railway/Fly.io would use the same `Procfile`, `wsgi.py` and `requirements.txt`.

## Notes / constraints

- Free PythonAnywhere has a daily CPU quota; adequate for a demo/pilot.
- The default subdomain has free HTTPS. If HTTPS is not active on your account, enable it in the **Web** tab (PythonAnywhere provides a free certificate).
- No database is used — scheme data lives in `data/schemes.json`, already included in the upload. All backend features (`/`, `/scheme`, `/sources`, `/ask`, `/api/schemes`, `/healthz`) work after deployment.
- To update content later, edit the local files and re-run the deployment script.
