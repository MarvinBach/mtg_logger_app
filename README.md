# MTG Game Logger

Eine Streamlit-App zum Tracken von Magic: The Gathering Spielen.

## Installation

1. Python-Umgebung erstellen:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Supabase-Konfiguration:
- Erstellen Sie eine `.env` Datei im Projektverzeichnis
- Fügen Sie Ihre Supabase-Zugangsdaten ein:
```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

4. App starten:
```bash
streamlit run app.py
```

Die App ist dann unter http://localhost:8501 verfügbar.
