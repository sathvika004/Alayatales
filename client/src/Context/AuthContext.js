import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        return localStorage.getItem('token') ? true : false;
    });

    const [userRole, setUserRole] = useState(() => {
        return localStorage.getItem('userRole') || null;
    });

    useEffect(() => {
        localStorage.setItem('userRole', userRole);
    }, [userRole]);

    const login = (token, role) => {
        localStorage.setItem('token', token);
        setIsAuthenticated(true);
        setUserRole(role);
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userRole');
        setIsAuthenticated(false);
        setUserRole(null);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, userRole, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};