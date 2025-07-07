import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';
import { TeamOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import { handleShowGroupList } from '../../handlers/user.jsx';

import styles from './GroupList.module.css';

const GroupList = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userGroups, setUserGroups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    handleShowGroupList(setUserGroups, setLoading, setError);
  }, []);

  const onClick = (e) => {
    if (e.key !== 'no-groups') {
      navigate(`/groups/${e.key}`);
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
      <div className={styles.container}>
          <div className={styles.title}>
              <TeamOutlined/>
              Мои группы
          </div>
          <div className={styles.card}>
            <Menu
              theme="dark"
              onClick={onClick}
              className={styles.menu}
              mode="inline"
              items={userGroups}
            />
          </div>
      </div>
  );
};

export default GroupList;