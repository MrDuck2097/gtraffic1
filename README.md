# GTraffic iOS Link Checker (starter)

This is an iPhone/Safari-friendly web interface plus a small Python backend.
It checks a normal HTTP redirect from a GTraffic URL. It intentionally does
not bypass CAPTCHA, submit verification codes, execute challenge scripts, or
evade anti-bot controls.

## Run / deploy
1. Deploy this folder to a Python host that supports Flask.
2. Install dependencies: `pip install -r requirements.txt`
3. Start: `python app.py`
4. Open the deployed HTTPS address in Safari and optionally use Share > Add to Home Screen.

The app cannot work as a standalone local HTML file because `/resolve` needs
the backend. Do not enter passwords, OTPs, or private verification codes.
