import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';

const AuthButton = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await axios.get('/api/v1/auth/check-auth', {
          withCredentials: true
        });

        setIsAuthenticated(response.data);
      } catch (error) {
        console.error('Ошибка проверки авторизации:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  if (loading) {
    return <div style={{ width: 100 }}>Загрузка...</div>;
  }

  return (
    <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '20px' }}>
      {isAuthenticated ? (
        <Link to="/profile">
          <Avatar
            size="large"
            icon={<UserOutlined />}
            style={{ backgroundColor: '#7a3ccb' }}
          />
        </Link>
      ) : (
        <Link
          to="/login"
          style={{
            fontSize: '20px',
            color: 'black',
            textDecoration: 'none'
          }}
        >
          Войти
        </Link>
      )}
    </div>
  );
};

export default AuthButton;
