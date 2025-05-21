import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

import Home from './pages/Home';
import Hello from './pages/Hello';
import Login from './pages/Login';
import Registration from './pages/Registration';
import Profile from './pages/Profile';
import Verify from './pages/Verify';

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/hello" element={<Hello />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/verify" element={<Verify />} />
      </Routes>
    </div>
  );
}
