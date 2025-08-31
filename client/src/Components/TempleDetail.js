import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTempleById } from '../Services/TempleService';

const TempleDetail = () => {
    const { id } = useParams();
    const [temple, setTemple] = useState(null);

    useEffect(() => {
        const fetchTemple = async () => {
            const data = await getTempleById(id);
            setTemple(data);
        };
        fetchTemple();
    }, [id]);

    if (!temple) {
        return <div>Loading...</div>;
    }

    return (
        <div className="temple-detail-page">
            <div className="image-gallery">
                {temple.images.map((image, index) => (
                    <img className="gallery-image" key={index} src={`http://localhost:5000${image}`} alt={`${temple.name} image ${index + 1}`} />
                ))}
            </div>
            <h2>{temple.name}</h2>
            <p>{temple.description}</p>
            <p><strong>Location:</strong> {temple.location}</p>
            {temple.timings.map((timing, index) => (
                <div key={index} style={{ marginBottom: '10px' }}>
                    <p><strong>Timings {index + 1}:</strong></p>
                    <p>Morning: {timing.morningOpening} - {timing.morningClosing}</p>
                    <p>Evening: {timing.eveningOpening} - {timing.eveningClosing}</p>
                </div>
            ))}
        </div>
    );
};

export default TempleDetail;