const Temple = require('../models/Temple');

// @desc    Get all temples
// @route   GET /api/temples
const getTemples = async (req, res) => {
    try {
        const temples = await Temple.find({});
        res.json(temples);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// @desc    Get a single temple by ID
// @route   GET /api/temples/:id
const getTempleById = async (req, res) => {
    try {
        const temple = await Temple.findById(req.params.id);
        if (temple) {
            res.json(temple);
        } else {
            res.status(404).json({ message: 'Temple not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// @desc    Create a new temple
// @route   POST /api/temples
const createTemple = async (req, res) => {
    try {
        const { name, description, location, timings } = req.body;
        const images = req.files.map(file => `/uploads/${file.filename}`); // Get paths for all uploaded images

        const newTemple = new Temple({
            name,
            description,
            location,
            timings: JSON.parse(timings), // Parse the timings string back into an array
            images,
        });
        const createdTemple = await newTemple.save();
        res.status(201).json(createdTemple);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// @desc    Update a temple
// @route   PUT /api/temples/:id
const updateTemple = async (req, res) => {
    try {
        const { name, description, location, timings } = req.body;
        const temple = await Temple.findById(req.params.id);

        if (temple) {
            temple.name = name || temple.name;
            temple.description = description || temple.description;
            temple.location = location || temple.location;
            temple.timings = JSON.parse(timings) || temple.timings;

            // Handle image update if new images are uploaded
            if (req.files && req.files.length > 0) {
                temple.images = req.files.map(file => `/uploads/${file.filename}`);
            }

            const updatedTemple = await temple.save();
            res.json(updatedTemple);
        } else {
            res.status(404).json({ message: 'Temple not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// @desc    Delete a temple
// @route   DELETE /api/temples/:id
const deleteTemple = async (req, res) => {
    try {
        const temple = await Temple.findById(req.params.id);
        if (temple) {
            await temple.deleteOne();
            res.json({ message: 'Temple removed' });
        } else {
            res.status(404).json({ message: 'Temple not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

module.exports = {
    getTemples,
    getTempleById,
    createTemple,
    updateTemple,
    deleteTemple
};