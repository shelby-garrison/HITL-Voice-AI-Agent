const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const requests = {};

// Creating a human request
app.post('/api/requests', (req, res) => {
  const { question } = req.body;
  const id = uuidv4();
  requests[id] = { question, answer: null, resolved: false };
  console.log(requests[id])
  console.log(`New request created: ${id} - "${question}"`);
  res.json({ request_id: id });
});

// Getting a single request status (for polling)
app.get('/api/requests/:id', (req, res) => {
  const { id } = req.params;
  if (!requests[id]) {
    return res.status(404).json({ error: 'Request not found' });
  }
  console.log(`Request ${id} status checked - resolved: ${requests[id].resolved}`);

  res.json(requests[id]);
});

// Listing all unresolved requests (dashboard)
app.get('/api/requests', (req, res) => {
  const pending = Object.entries(requests)
    .filter(([, v]) => !v.resolved)
    .map(([id, v]) => ({ id, question: v.question }));
  res.json(pending);
});

// Human sends an answer
app.post('/api/requests/:id/answer', (req, res) => {
  const { id } = req.params;
  const { answer } = req.body;
  
  if (!requests[id]) return res.status(404).json({ error: 'Request not found' });
  
  requests[id].answer = answer;
  requests[id].resolved = true;
  
  console.log(`Answer provided for request ${id}: "${answer}"`);
  res.json({ success: true });
});

app.listen(PORT, () => console.log(`✅ Server running at http://localhost:${PORT}`));