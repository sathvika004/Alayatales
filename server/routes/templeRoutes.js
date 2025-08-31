const express = require('express');
const router = express.Router();
const multer = require('multer');
const {
    getTemples,
    getTempleById,
    createTemple,
    updateTemple,
    deleteTemple
} = require('../controllers/templeController');

// Multer storage configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});

const upload = multer({ storage });

// Routes for all temples
router.route('/')
    .get(getTemples)
    .post(upload.array('images', 5), createTemple); // Changed to upload.array

// Routes for a single temple
router.route('/:id')
    .get(getTempleById)
    .put(upload.array('images', 5), updateTemple) // Changed to upload.array
    .delete(deleteTemple);

module.exports = router;