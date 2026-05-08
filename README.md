# Marshal Deobfuscator v2.5 (Modular)

Modular version with clean structure.

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Deploy on Render
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --workers 2 --threads 4`
```

Now create a zip of this new modular version.