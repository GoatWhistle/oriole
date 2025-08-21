import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';

import { fetchCheckAuth } from '../../../api/check_auth.jsx';
import styles from './AuthButton.module.css';

const AuthButton = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const authResponse = await fetchCheckAuth();
        setIsAuthenticated(authResponse.isAuthenticated);
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Загрузка...</div>;
  }

  return (
    <div className={styles.container}>
      {isAuthenticated ? (
        <Link to="/profile">
          <Avatar
            size="large"
            icon={<UserOutlined />}
            className={styles.avatar}
          />
        </Link>
      ) : (
        <Link to="/login" className={styles.link}>
          Войти
        </Link>
      )}
    </div>
  );
};

export default AuthButton;
