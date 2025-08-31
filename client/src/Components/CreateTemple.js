import React, { useState } from 'react';
import axios from 'axios';

const CreateTemple = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    location: '',
    openingTime: '',
    closingTime: ''
  });
  const [image, setImage] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('name', formData.name);
    data.append('description', formData.description);
    data.append('location', formData.location);
    data.append('openingTime', formData.openingTime);
    data.append('closingTime', formData.closingTime);
    data.append('image', image);

    try {
      await axios.post('http://localhost:5000/api/temples', data);
      alert('Temple added successfully!');
      // Reset form
      setFormData({ name: '', description: '', location: '', openingTime: '', closingTime: '' });
      setImage(null);
    } catch (error) {
      console.error(error);
      alert('Error adding temple.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Add New Temple</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Temple Name" required /><br/>
        <textarea name="description" value={formData.description} onChange={handleChange} placeholder="Description" required></textarea><br/>
        <input type="text" name="location" value={formData.location} onChange={handleChange} placeholder="Location" required /><br/>
        <input type="text" name="openingTime" value={formData.openingTime} onChange={handleChange} placeholder="Opening Time" required /><br/>
        <input type="text" name="closingTime" value={formData.closingTime} onChange={handleChange} placeholder="Closing Time" required /><br/>
        <input type="file" name="image" onChange={handleImageChange} required /><br/>
        <button type="submit">Add Temple</button>
      </form>
    </div>
  );
};

export default CreateTemple;