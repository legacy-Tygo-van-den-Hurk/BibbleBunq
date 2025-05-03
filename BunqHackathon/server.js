const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// POST endpoint for safety check
app.post('/safety-check', (req, res) => {
  const { city } = req.body;
  console.log(`Received safety check request for city: ${city}`);

  res.json({
    city,
  });
});

// Listen on all interfaces
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}`);
});
