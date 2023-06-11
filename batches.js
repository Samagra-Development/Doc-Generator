const express = require('express');
const { v4: uuidv4 } = require('uuid');
const app = express();

// Define a global array to store the created batches
let batches = [];

// Middleware to parse JSON request bodies
app.use(express.json());

// POST /batches endpoint to create a new batch
app.post('/batches', (req, res) => {
  const { template, data, engineType, templateType, outputType } = req.body;

  // Generate a unique ID for the batch
  const batchId = uuidv4();

  // Create a new batch object
  const newBatch = {
    id: batchId,
    template,
    data,
    engineType,
    templateType,
    outputType,
    status: 'submitted',
  };

  // Add the new batch to the batches array
  batches.push(newBatch);

  // Return the created batch in the response
  res.status(201).json(newBatch);
});

// Start the server
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
