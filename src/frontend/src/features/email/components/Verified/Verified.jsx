import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Typography } from 'antd';

import { handleVerify } from '../../handlers/user.jsx';

import styles from './Verified.module.css';

const { Title } = Typography;

const Verified = () => {
  const { token } = useParams();

  useEffect(() => {
    handleVerify(token);
  }, [token]);

  return (
    <div className={styles.container}>
      {status === 'loading' && <p className={styles.loading}>Verifying...</p>}

      {status === 'success' && (
        <div className={styles.successContainer}>
          <div className={styles.card}>
            <Title level={2} className={styles.title}>
              Ваша почта подтверждена!
            </Title>
            <Link to="/" className={styles.link}>
              Перейти на главную страницу
            </Link>
          </div>
        </div>
      )}

      {status === 'error' && (
        <div className={styles.errorContainer}>
          <div className={styles.errorCard}>
            <Title level={2} className={styles.errorTitle}>
              Ошибка подтверждения
            </Title>
            <p className={styles.errorMessage}>{message}</p>
            <Link to="/" className={styles.link}>
              Вернуться на главную
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Verified;
