import React, { useState, useEffect } from 'react';
import { getTemples, deleteTemple } from '../Services/TempleService';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
    const [temples, setTemples] = useState([]);

    useEffect(() => {
        fetchTemples();
    }, []);

    const fetchTemples = async () => {
        const data = await getTemples();
        setTemples(data);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this temple?')) {
            await deleteTemple(id);
            fetchTemples(); // Refresh the list
        }
    };

    return (
        <div>
            <h2>Admin Dashboard</h2>
            <Link to="/admin/create">Add New Temple</Link>
            <div className="temple-admin-list">
                {temples.map((temple) => (
                    <div key={temple._id} className="admin-temple-row">
                        <span>{temple.name}</span>
                        <div>
                            <Link to={`/admin/edit/${temple._id}`}>Edit</Link>
                            <button onClick={() => handleDelete(temple._id)}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminDashboard;