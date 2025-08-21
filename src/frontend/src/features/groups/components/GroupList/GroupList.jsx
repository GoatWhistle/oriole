import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';
import { TeamOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import { handleShowGroupList } from '../../handlers/user.jsx';

import styles from './GroupList.module.css';

const GroupList = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userGroups, setUserGroups] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserGroups = async () => {
      try {
        setLoading(true);
        const response = await handleShowGroupList();

        if (response.status === 200) {
          setIsAuthenticated(true);
          setUserGroups(response.data.data || []);
        } else if (response.status === 401) {
          setIsAuthenticated(false);
        } else {
          throw new Error(response.data?.message || 'Ошибка при загрузке групп');
        }
      } catch (err) {
        setError(err.message);
        message.error(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserGroups();
  }, []);

  const onClick = (e) => {
    if (e.key !== 'no-groups') {
      navigate(`/groups/${e.key}`);
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;

  if (!isAuthenticated) {
    return (
      <div className={styles.container}>
        <div className={styles.title}>
          <TeamOutlined />
          Мои группы
        </div>
        <div className={styles.card}>
          <div className={styles.notAuthMessage}>
            Войдите, чтобы увидеть список своих групп
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className={styles.error}>Ошибка: {error}</div>;
  }

  const menuItems = userGroups.length > 0
    ? userGroups.map(group => ({
        key: group.id,
        label: group.name,
        icon: <TeamOutlined />,
      }))
    : [{
        key: 'no-groups',
        label: 'У вас пока нет групп',
        disabled: true,
      }];

  return (
    <div className={styles.container}>
      <div className={styles.title}>
        <TeamOutlined />
        Мои группы
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

export default GroupList;