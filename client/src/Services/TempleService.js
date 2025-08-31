import axios from 'axios';

const API_URL = 'http://localhost:5000/api/temples';

// Get all temples
export const getTemples = async () => {
    const response = await axios.get(API_URL);
    return response.data;
};

// Get a single temple by ID
export const getTempleById = async (id) => {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
};

// Create a new temple
export const createTemple = async (templeData) => {
    const formData = new FormData();
    formData.append('name', templeData.name);
    formData.append('description', templeData.description);
    formData.append('location', templeData.location);
    // Stringify the timings array to send it as form-data
    formData.append('timings', JSON.stringify(templeData.timings)); 
    // Append each image to the form data
    for (let i = 0; i < templeData.images.length; i++) {
        formData.append('images', templeData.images[i]);
    }

    const response = await axios.post(API_URL, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Update a temple
export const updateTemple = async (id, templeData) => {
    const formData = new FormData();
    formData.append('name', templeData.name);
    formData.append('description', templeData.description);
    formData.append('location', templeData.location);
    formData.append('timings', JSON.stringify(templeData.timings));
    
    // Append each new image to the form data
    if (templeData.images) {
        for (let i = 0; i < templeData.images.length; i++) {
            formData.append('images', templeData.images[i]);
        }
    }

    const response = await axios.put(`${API_URL}/${id}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Delete a temple
export const deleteTemple = async (id) => {
    await axios.delete(`${API_URL}/${id}`);
};