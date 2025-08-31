import React, { useState, useEffect } from 'react';
import { getTempleById, updateTemple } from '../Services/TempleService';
import { useNavigate, useParams } from 'react-router-dom';

const EditTemple = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        location: '',
        timings: [{ morningOpening: '', morningClosing: '', eveningOpening: '', eveningClosing: '' }],
        images: null,
    });

    useEffect(() => {
        const fetchTemple = async () => {
            const templeData = await getTempleById(id);
            setFormData({
                name: templeData.name,
                description: templeData.description,
                location: templeData.location,
                timings: templeData.timings,
                images: null,
            });
        };
        fetchTemple();
    }, [id]);

    const handleChange = (e) => {
        if (e.target.name === 'images') {
            setFormData({ ...formData, images: e.target.files });
        } else {
            setFormData({ ...formData, [e.target.name]: e.target.value });
        }
    };

    const handleTimingsChange = (e, index) => {
        const newTimings = [...formData.timings];
        newTimings[index] = { ...newTimings[index], [e.target.name]: e.target.value };
        setFormData({ ...formData, timings: newTimings });
    };

    const addTimings = () => {
        setFormData({
            ...formData,
            timings: [...formData.timings, { morningOpening: '', morningClosing: '', eveningOpening: '', eveningClosing: '' }]
        });
    };

    const removeTimings = (index) => {
        const newTimings = [...formData.timings];
        newTimings.splice(index, 1);
        setFormData({ ...formData, timings: newTimings });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updateTemple(id, formData);
            alert('Temple updated successfully!');
            navigate('/admin');
        } catch (error) {
            alert('Error updating temple.');
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Edit Temple</h2>
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Name" required />
            <textarea name="description" value={formData.description} onChange={handleChange} placeholder="Description" required></textarea>
            <input type="text" name="location" value={formData.location} onChange={handleChange} placeholder="Location" required />

            <h3>Timings:</h3>
            {formData.timings.map((timing, index) => (
                <div key={index}>
                    <input type="text" name="morningOpening" value={timing.morningOpening} onChange={(e) => handleTimingsChange(e, index)} placeholder="Morning Opening" required />
                    <input type="text" name="morningClosing" value={timing.morningClosing} onChange={(e) => handleTimingsChange(e, index)} placeholder="Morning Closing" required />
                    <input type="text" name="eveningOpening" value={timing.eveningOpening} onChange={(e) => handleTimingsChange(e, index)} placeholder="Evening Opening" required />
                    <input type="text" name="eveningClosing" value={timing.eveningClosing} onChange={(e) => handleTimingsChange(e, index)} placeholder="Evening Closing" required />
                    <button type="button" onClick={() => removeTimings(index)}>Remove</button>
                </div>
            ))}
            <button type="button" onClick={addTimings}>Add More Timings</button>

            <p>Upload new images to replace existing ones:</p>
            <input type="file" name="images" multiple onChange={handleChange} />
            <button type="submit">Update Temple</button>
        </form>
    );
};

export default EditTemple;