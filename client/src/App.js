import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Components/HomePage';
import TempleDetail from './Components/TempleDetail';
import AdminDashboard from './Components/AdminDashboard';
import AddTemple from './Components/AddTemple';
import EditTemple from './Components/EditTemple';
import Login from './Components/Login';
import Register from './Components/Register';
import Header from './Components/Header';
import ProtectedRoute from './Components/ProtectedRoute';
import { AuthProvider } from './Context/AuthContext';
import Profile from './Components/Profile'; // Import the Profile component
import './App.css';

function App() {
    return (
        <Router>
            <AuthProvider>
                <div className="App">
                    <Header />
                    <main>
                        <Routes>
                            {/* Public routes */}
                            <Route path="/" element={<HomePage />} />
                            <Route path="/temple/:id" element={<TempleDetail />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />

                            {/* Protected routes */}
                            <Route element={<ProtectedRoute />}>
                                <Route path="/admin" element={<AdminDashboard />} />
                                <Route path="/admin/create" element={<AddTemple />} />
                                <Route path="/admin/edit/:id" element={<EditTemple />} />
                                <Route path="/profile" element={<Profile />} /> {/* The new protected route */}
                            </Route>
                        </Routes>
                    </main>
                </div>
            </AuthProvider>
        </Router>
    );
}

export default App;