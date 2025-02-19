const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = process.env.PORT || 3001;
const morgan = require('morgan');
const cors = require('cors');

app.use(
  cors({
    origin: 'http://localhost:3000',
  })
);
app.use(morgan('dev'));
app.use(express.json()); // parse JSON entity

// read db.json
const dbPath = path.join(__dirname, 'db.json');

// API: search clients by first name
app.get('/api/clients/search', (req, res) => {
  console.log('Received request for search with query:', req.query);

  const { firstName } = req.query;
  console.log('first name:', firstName);
  if (!firstName) {
    return res.status(400).json({ error: 'Name query parameter is required' });
  }

  // Read the clients data from db.json
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }

    let db;
    try {
      db = JSON.parse(data);
    } catch (parseError) {
      console.error('Error parsing database JSON:', parseError);
      return res.status(500).json({ message: 'Error parsing database' });
    }

    const clients = db['form-submissions'] || []; // Ensure the clients array exists
    //console.log('All clients:', clients); // Log all clients before filtering

    // Filter clients by first name (case insensitive)
    const matchingClients = clients.filter((client) => {
      const clientFirstName = client.firstName; // Get the client's first name
      return clientFirstName.toLowerCase() === firstName.toLowerCase();
    });

    console.log('Matching clients:', matchingClients);
    res.json(matchingClients);
  });
});

// API: get user details by ID
app.get('/api/client/:id', (req, res) => {
  const userId = req.params.id;

  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }

    const db = JSON.parse(data);
    const user = db['form-submissions'].find((user) => user.id === userId);

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json(user);
  });
});

function generateUniqueId(length = 4) {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    result += characters[randomIndex];
  }
  return result;
}

// API: create new user info form
app.post('/api/submit-form', (req, res) => {
  const formData = req.body;

  // Generate a unique ID for the new form submission
  const newSubmission = {
    id: generateUniqueId(), // Generate a 4-character unique ID
    ...formData,
  };

  // Read existing submissions
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }

    const db = JSON.parse(data);
    db['form-submissions'] = db['form-submissions'] || []; // Ensure the array exists
    db['form-submissions'].push(newSubmission); // Add the new submission

    // Write back to db.json
    fs.writeFile(dbPath, JSON.stringify(db, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ message: 'Error saving form submission' });
      }
      res.status(201).json({
        message: 'Form submitted successfully',
        submission: newSubmission,
      });
    });
  });
});

// API: read user info
app.get('/api/users', (req, res) => {
  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }
    const db = JSON.parse(data);
    res.json(db['form-submissions']);
  });
});

// API: update user info
app.put('/api/update-user/:id', (req, res) => {
  const userId = req.params.id;
  const updatedData = req.body;

  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }
    const db = JSON.parse(data);
    const userIndex = db['form-submissions'].findIndex((user) => user.id === userId);

    if (userIndex === -1) {
      return res.status(404).json({ message: 'User not found' });
    }

    // update user info
    db['form-submissions'][userIndex] = {
      ...db['form-submissions'][userIndex],
      ...updatedData,
    };

    // write back to db.json
    fs.writeFile(dbPath, JSON.stringify(db, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ message: 'Error updating database' });
      }
      res.json({ message: 'User updated successfully', userId, updatedData });
    });
  });
});

// API: placeholder api for back to work score calculation
app.post('/api/work-score', (req, res) => {
  let score = 20; // base line score

  // give the fields default values if they are undefined
  const userData = {
    work_experience: req.body.work_experience ?? 0,
    canada_workex: req.body.canada_workex ?? 0,
    age: req.body.age,
    reading_english_scale: req.body.reading_english_scale ?? 0,
    speaking_english_scale: req.body.speaking_english_scale ?? 0,
    writing_english_scale: req.body.writing_english_scale ?? 0,
    numeracy_scale: req.body.numeracy_scale ?? 0,
    computer_scale: req.body.computer_scale ?? 0,
    felony_bool: req.body.felony_bool ?? 'false',
    substance_use: req.body.substance_use ?? 'false',
    need_mental_health_support_bool: req.body.need_mental_health_support_bool ?? 'false',
    transportation_bool: req.body.transportation_bool ?? 'false',
    currently_employed: req.body.currently_employed ?? 'false',
  };

  score += Math.min(userData.work_experience, 10);
  score += Math.min(userData.canada_workex, 5);

  if (userData.age >= 18 && userData.age <= 35) {
    score += 5;
  } else if (userData.age <= 50) {
    score += 3;
  }

  score += Math.min(userData.reading_english_scale, 10);
  score += Math.min(userData.speaking_english_scale, 10);
  score += Math.min(userData.writing_english_scale, 10);
  score += Math.min(userData.numeracy_scale, 10);
  score += Math.min(userData.computer_scale, 10);

  // Deduct points for certain conditions
  if (userData.felony_bool === 'true') { score -= 5; }
  if (userData.substance_use === 'true') { score -= 3; }
  if (userData.need_mental_health_support_bool === 'true') { score -= 2; }

  // Add bonus points for having transportation or being currently employed
  if (userData.transportation_bool === 'true') { score += 2; }
  if (userData.currently_employed === 'true') { score += 5; }

  score = Math.max(score, 0);
  score = Math.min(score, 100);

  res.json({
    baseline: score,
    interventions: [
      [8.5, ['Job training']],
      [6.3, ['Counseling']],
      [5.0, ['Mentorship programs']],
    ],
  });
});

// API: delete user info for test
app.delete('/api/delete-user/:id', (req, res) => {
  const userId = req.params.id;

  fs.readFile(dbPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ message: 'Error reading database' });
    }
    const db = JSON.parse(data);
    const userIndex = db['form-submissions'].findIndex((user) => user.id === userId);

    if (userIndex === -1) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Remove the user from the submissions
    db['form-submissions'].splice(userIndex, 1);

    // Write back to db.json
    fs.writeFile(dbPath, JSON.stringify(db, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ message: 'Error updating database' });
      }
      res.json({ message: 'User deleted successfully', userId });
    });
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
