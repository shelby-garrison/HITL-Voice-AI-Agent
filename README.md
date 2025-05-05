
##  LiveKit Assistant Setup

###  1. Create Virtual Environment & Install Dependencies

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Use `source .venv/bin/activate` on Linux/Mac

# Upgrade pip and install required Python packages
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

###  2. Set Environment Variables

Create a `.env` file in the project root and add:

```env
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
GROQ_API_KEY=your_groq_api_key
```

---

###  3. Run the Assistant

```bash
python main.py download-files
python main.py start
```
You can access the agent via https://agents-playground.livekit.io/
---

###  4. Run Dashboard Server (Port 5000)

 Installing dependencies:
```bash
npm install
```

Running dashboard server:

```bash
# From the dashboard directory
cd dashboard
node server.js
```

The dashboard will be live at: [http://localhost:5000](http://localhost:5000)

---


