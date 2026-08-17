# Network Command Assistant v2

## Local run
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000

## Version 2
- Weighted search
- Cisco / FortiGate / Palo Alto vendor filter
- Command detail pages
- What-to-check guidance
- Cross-vendor comparison
- Mobile-friendly layout
- Render deployment files
- /health endpoint

## Deploy with GitHub + Render
1. Create a GitHub repository named network-command-assistant.
2. Upload the contents of this project folder.
3. In Render, create a new Web Service and connect that GitHub repository.
4. Build command: pip install -r requirements.txt
5. Start command: gunicorn app:app
6. Deploy.
7. Render will provide a public HTTPS URL.

Important: this is a learning/demo command dataset. Verify commands against documentation for the exact vendor platform and software version before production use.
