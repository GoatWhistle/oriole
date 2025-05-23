import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

import Home from './pages/Home';
import Hello from './pages/Hello';
import Login from './pages/Login';
import Registration from './pages/Registration';
import Profile from './pages/Profile';
import Verify from './pages/Verify';
import Assignment from './pages/Assignment';
import Group from './pages/Group';
import JoinGroup from './pages/JoinGroup';

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/hello" element={<Hello />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/verify/:token" element={<Verify />} />
        <Route path="/assignment/:assignment_id" element={<Assignment />} />
        <Route path="/group/:group_id" element={<Group />} />
        <Route path="/groups/join/:code" element={<JoinGroup />} />
      </Routes>
    </div>
  );
}
