import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TempleList = () => {
  const [temples, setTemples] = useState([]);

  useEffect(() => {
    const fetchTemples = async () => {
      const res = await axios.get('http://localhost:5000/api/temples');
      setTemples(res.data);
    };
    fetchTemples();
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Alayatales</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem' }}>
        {temples.map((temple) => (
          <div key={temple._id} style={{ border: '1px solid #ccc', padding: '1rem', width: '300px' }}>
            <img src={`http://localhost:5000${temple.image}`} alt={temple.name} style={{ width: '100%', height: '200px', objectFit: 'cover' }} />
            <h3>{temple.name}</h3>
            <p>{temple.description.substring(0, 100)}...</p>
            <p><strong>Location:</strong> {temple.location}</p>
            <p><strong>Timing:</strong> {temple.openingTime} - {temple.closingTime}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TempleList;