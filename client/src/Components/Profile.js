import React, { useState, useEffect } from 'react';
import { getUserProfile } from '../Services/UserService';

const Profile = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const profileData = await getUserProfile();
                setUser(profileData);
            } catch (error) {
                console.error("Failed to fetch user profile:", error);
            }
        };
        fetchProfile();
    }, []);

    if (!user) {
        return <div>Loading profile...</div>;
    }

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>User Profile</h2>
            <p><strong>Username:</strong> {user.username}</p>
        </div>
    );
};

export default Profile;