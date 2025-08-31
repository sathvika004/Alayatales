const mongoose = require('mongoose');

const TempleSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: true,
    },
    location: {
        type: String,
        required: true,
    },
    timings: {
        type: [
            {
                morningOpening: { type: String, required: true },
                morningClosing: { type: String, required: true },
                eveningOpening: { type: String, required: true },
                eveningClosing: { type: String, required: true },
            }
        ],
        required: true,
    },
    images: {
        type: [String], // Change to an array of strings
        required: true,
    },
});

module.exports = mongoose.model('Temple', TempleSchema);