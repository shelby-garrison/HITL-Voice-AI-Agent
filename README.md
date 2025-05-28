# Human-in-the-Loop Voice AI Agent

This project is a locally running prototype of a human-in-the-loop AI system that interacts with customers over phone calls. It escalates queries to a human supervisor when it doesn't know the answer, follows up with the customer, and updates its internal knowledge base accordingly.

## 🔧 Functionalities

### 1. AI Agent Setup (via LiveKit)
- Simulated AI agent initialized with basic business info about a fake salon.
- Handles incoming calls using LiveKit.
- Responds to known questions directly.
- Triggers an event for unknown queries when human assistance is needed.

### 2. Human Request Handling
- Creates a structured help request to human supervisor.
- Simulates notifying a supervisor via console logs and webhooks

### 3. Supervisor Response Interface
- Web-based UI for supervisors to:
  - View all pending help requests
  - Submit answers to queries
  
- Once answered:
  - AI sends follow-up to original caller.
  - Answer is saved to the knowledge base of the voice AI agent.


 **SETUP INSTRUCTIONS**
 
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


