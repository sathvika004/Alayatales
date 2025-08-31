import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../Context/AuthContext';

const ProtectedRoute = () => {
    const { isAuthenticated } = useContext(AuthContext);

    // If authenticated, render the child routes (Outlet)
    // Otherwise, redirect to the login page
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;