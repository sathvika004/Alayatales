const express = require('express');
const router = express.Router();
const { protect } = require('../middleware/authMiddleware'); // Import the middleware
const { registerUser, authUser, getUserProfile } = require('../controllers/userController'); // Add getUserProfile

router.post('/register', registerUser);
router.post('/login', authUser);
router.route('/profile').get(protect, getUserProfile); // Protected route

module.exports = router;