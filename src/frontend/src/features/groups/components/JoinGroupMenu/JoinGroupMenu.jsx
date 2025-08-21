import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Typography, Button, Result, Spin } from 'antd';

import { handleJoinGroup } from '../../handlers/group.jsx';

import styles from './JoinGroupMenu.module.css';

const { Text } = Typography;

const JoinGroupMenu = () => {
  const { invite_code } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    handleJoinGroup(invite_code, setResult, setError, setLoading);
  }, [invite_code]);

  const handleNavigateToGroup = () => {
    navigate(result?.group_id ? `/groups/${result.group_id}` : '/');
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" tip="Обработка приглашения..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <Card className={styles.card}>
          <Result
            status="error"
            title="Ошибка вступления в группу"
            subTitle={error}
            extra={[
              <Button type="primary" key="home" onClick={() => navigate('/')}>
                На главную
              </Button>
            ]}
          />
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card className={styles.card}>
        <Result
          status="success"
          title="Вы вступили в группу!"
          subTitle={
            <Text>
              Теперь вы участник группы. Можете перейти к просмотру заданий и участников.
            </Text>
          }
          extra={[
            <Button
              type="primary"
              key="group"
              onClick={handleNavigateToGroup}
              className={styles.groupButton}
            >
              Перейти в группу
            </Button>,
            <Button key="home" onClick={() => navigate('/')}>
              На главную
            </Button>
          ]}
        />
      </Card>
    </div>
  );
};

export default JoinGroupMenu;
