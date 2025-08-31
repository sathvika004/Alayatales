const User = require('../models/User');

const adminProtect = async (req, res, next) => {
    // Check if the authenticated user's role is 'admin'
    if (req.user && req.user.role === 'admin') {
        next();
    } else {
        res.status(403).json({ message: 'Forbidden: Admin access required' });
    }
};

module.exports = { adminProtect };