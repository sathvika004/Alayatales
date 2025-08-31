import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Context/AuthContext';

const Header = () => {
    const { isAuthenticated, userRole, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <header style={{ padding: '1rem', backgroundColor: '#333', color: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 style={{ margin: 0 }}>Alayatales</h1>
            <nav>
                <Link to="/" style={{ color: '#fff', marginRight: '1rem', textDecoration: 'none' }}>Home</Link>
                {isAuthenticated ? (
                    <>
                        {userRole === 'admin' && (
                            <Link to="/admin" style={{ color: '#fff', marginRight: '1rem', textDecoration: 'none' }}>Admin Dashboard</Link>
                        )}
                        <Link to="/profile" style={{ color: '#fff', marginRight: '1rem', textDecoration: 'none' }}>Profile</Link>
                        <button onClick={handleLogout} style={{ background: 'none', border: '1px solid white', color: 'white', padding: '8px 12px', borderRadius: '4px', cursor: 'pointer' }}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" style={{ color: '#fff', marginRight: '1rem', textDecoration: 'none' }}>Login</Link>
                        <Link to="/register" style={{ color: '#fff', textDecoration: 'none' }}>Register</Link>
                    </>
                )}
            </nav>
        </header>
    );
};

export default Header;