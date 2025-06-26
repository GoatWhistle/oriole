import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

import Home from '../pages/Home';
import Hello from '../pages/Hello';
import Login from '../pages/Login';
import Registration from '../pages/Registration';
import Profile from '../pages/Profile';
import Verify from '../pages/Verify';
import Module from '../pages/Module';
import Group from '../pages/Group';
import JoinGroup from '../pages/JoinGroup';
import ForgotPassword from '../pages/ForgotPassword';
import ResetPassword from '../pages/ResetPassword';
import Task from '../pages/Task';

import './App.css';

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
          <Route path="/modules/:module_id" element={<Module />} />
          <Route path="/groups/:group_id" element={<Group />} />
          <Route path="/groups/join/:invite_code" element={<JoinGroup />} />
          <Route path="/forgot_password_redirect/:token" element={<ForgotPassword />} />
          <Route path="/reset_password_redirect/:token" element={<ResetPassword />} />
          <Route path="/tasks/:task_id" element={<Task />} />
        </Routes>
    </div>
  );
}
