import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';
import { CalculatorOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import { handleShowModuleList } from '../../handlers/user.jsx';

import styles from './ModuleList.module.css';

const ModuleList = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userModules, setUserModules] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserModules = async () => {
      try {
        setLoading(true);
        const response = await handleShowModuleList();

        if (response.status === 200) {
          setIsAuthenticated(true);
          setUserModules(response.data.data || []);
        } else if (response.status === 401) {
          setIsAuthenticated(false);
        } else {
          throw new Error(response.data?.message || 'Ошибка при загрузке модулей');
        }
      } catch (err) {
        setError(err.message);
        message.error(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserModules();
  }, []);

  const onClick = (e) => {
    if (e.key !== 'no-modules') {
      navigate(`/modules/${e.key}`);
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;

  if (!isAuthenticated) {
    return (
      <div className={styles.container}>
        <div className={styles.title}>
          <CalculatorOutlined />
          Мои модули
        </div>
        <div className={styles.card}>
          <div className={styles.notAuthMessage}>
            Войдите, чтобы увидеть список своих модулей
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className={styles.error}>Ошибка: {error}</div>;
  }

  const menuItems = userModules.length > 0
    ? userModules.map(module => ({
        key: module.id,
        label: module.name,
        icon: <CalculatorOutlined />,
      }))
    : [{
        key: 'no-modules',
        label: 'У вас пока нет модулей',
        disabled: true,
      }];

  return (
    <div className={styles.container}>
      <div className={styles.title}>
        <CalculatorOutlined />
        Мои модули
      </div>
      <div className={styles.card}>
        <Menu
          theme="dark"
          onClick={onClick}
          className={styles.menu}
          mode="inline"
          items={menuItems}
        />
      </div>
    </div>
  );
};

export default ModuleList;