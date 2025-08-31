import React, { useState, useEffect } from 'react';
import { getTemples } from '../Services/TempleService';
import { Link } from 'react-router-dom';

const HomePage = () => {
    const [temples, setTemples] = useState([]);

    useEffect(() => {
        const fetchTemples = async () => {
            const data = await getTemples();
            setTemples(data);
        };
        fetchTemples();
    }, []);

    return (
        <div>
            <h2>All Temples</h2>
            <div className="temple-list">
                {temples.map((temple) => (
                    <div key={temple._id} className="temple-card">
                        {/* Display the first image as a thumbnail */}
                        <img src={`http://localhost:5000${temple.images[0]}`} alt={temple.name} />
                        <h3>{temple.name}</h3>
                        <p>{temple.description.substring(0, 100)}...</p>
                        <Link to={`/temple/${temple._id}`}>View Details</Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomePage;