const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const cors = require('cors');

const app = express();

// Middleware setup
app.use(bodyParser.json());
app.use(cors());

app.use(express.static('public'));

// MongoDB Atlas connection string
const connectionString = 'mongodb+srv://Remy:1234@cluster0.vgzdbrr.mongodb.net/Login_details?retryWrites=true&w=majority';

// Connect to MongoDB Atlas
mongoose.connect(connectionString, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
      // Avoid deprecation warning
})
.then(() => {
    console.log('Connected to MongoDB Atlas');
})
.catch((error) => {
    console.error('Error connecting to MongoDB Atlas:', error.message);
});

// User schema and model
const userSchema = new mongoose.Schema({
    fullName: String,
    email: { type: String, unique: true },
    password: String
});
const User = mongoose.model('user', userSchema); 

// Root Endpoint
app.get('/', (req, res) => {
    res.send('Server is up and running!');
});

// Register route
app.post('/register', async (req, res) => {
    try {
        const { fullName, email, password } = req.body;

        // Check if email already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ message: 'Email already exists' });
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const newUser = new User({
            fullName,
            email,
            password: hashedPassword
        });

        const savedUser = await newUser.save();
        if (savedUser) {
            console.log("User saved successfully:", savedUser);
            return res.status(201).json({ message: 'User registered successfully' });
        } else {
            console.log("Failed to save user.");
            return res.status(500).json({ error: 'Failed to save user' });
        }

    } catch (error) {
        console.error("Error in /register:", error);
        return res.status(500).json({ error: error.message });
    }
});

// Login route
app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ message: 'User not found' });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }

        // You could generate a token here if you want to implement JWT authentication
        res.status(200).json({ message: 'Login successful' });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Catch-all 404 Route
app.use('*', (req, res) => {
    res.status(404).send('Page not found');
});

// Starting the server
const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

