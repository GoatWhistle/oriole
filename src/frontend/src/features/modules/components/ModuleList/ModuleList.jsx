import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';
import { useNavigate } from 'react-router-dom';

import { handleShowModuleList } from '../../handlers/user.jsx';

import styles from './ModuleList.module.css';

const ModuleList = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userModules, setUserModules] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    handleShowModuleList(setUserModules, setLoading);
  }, []);

  const onClick = (e) => {
    if (e.key !== 'no-modules') {
      navigate(`/modules/${e.key}`);
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <Menu
      onClick={onClick}
      className={styles.menu}
      mode="inline"
      items={userModules}
    />
  );
};

export default ModuleList;