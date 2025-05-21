import React, { useState } from 'react';
import { Typography } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Title } = Typography;

export default function Verified() {

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: '#f0f2f5'
    }}>
      <div style={{
        background: '#fff',
        padding: '32px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        width: '450px'
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Ваша почта подтверждена!</Title>
        <Link to="/" style={{ fontWeight: 500 }}>Перейти на главную страницу</Link>
      </div>
    </div>
  );

};
