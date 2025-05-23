import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Button, Form, Input, message, Typography, Divider, Row, Col } from 'antd';
const { Title } = Typography;
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function Verify() {
  const { token } = useParams();
  const [status, setStatus] = useState('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await axios.get(`/api/v1/verify/${token}`);
        setStatus('success');
        setMessage(response.data.message);
      } catch (error) {
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Verification failed');
      }
    };

    verifyEmail();
  }, [token]);

  return (
    <div>
      {status === 'loading' && <p>Verifying...</p>}
      {status === 'success' &&
            (<div style={{
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
          )
      }
      {status === 'error' && <div className="error">{message}</div>}
    </div>
  );
}
