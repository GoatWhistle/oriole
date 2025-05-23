import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Result,
  Button,
  Spin,
  Alert,
  Typography
} from 'antd';
import axios from 'axios';

const { Title, Paragraph } = Typography;

const JoinGroupMenu = () => {
  const { invite_code } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const joinGroup = async () => {
      try {
        setLoading(true);
        const response = await axios.post(
          `/api/v1/groups/join/${invite_code}`,
          {},
          {
            withCredentials: true, // Для отправки cookies с аутентификацией
          }
        );

        if (response.data?.group_id) {
          // Если успешно - перенаправляем на страницу группы
          navigate(`/group/${response.data.group_id}`);
        } else {
          setResult({
            status: 'info',
            title: 'Приглашение обработано',
            message: response.data?.message || 'Вы успешно присоединились к группе'
          });
        }
      } catch (err) {
        console.error('Ошибка при присоединении к группе:', err);

        let errorMessage = 'Произошла ошибка при обработке приглашения';
        let errorStatus = 'error';

        if (err.response) {
          switch (err.response.status) {
            case 401:
              errorMessage = 'Требуется авторизация';
              break;
            case 403:
              errorMessage = 'Доступ запрещен';
              break;
            case 404:
              errorMessage = 'Приглашение не найдено или уже использовано';
              errorStatus = 'warning';
              break;
            case 409:
              errorMessage = 'Вы уже состоите в этой группе';
              errorStatus = 'info';
              break;
            default:
              errorMessage = err.response.data?.detail || errorMessage;
          }
        }

        setError({
          status: errorStatus,
          message: errorMessage,
          statusCode: err.response?.status
        });
      } finally {
        setLoading(false);
      }
    };

    joinGroup();
  }, [invite_code, navigate]);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '24px' }}>
        <Spin size="large" tip="Обработка приглашения..." />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '24px' }}>
        <Result
          status={error.status}
          title={`Ошибка ${error.statusCode || ''}`}
          subTitle={error.message}
          extra={[
            <Button
              type="primary"
              key="home"
              onClick={() => navigate('/')}
            >
              На главную
            </Button>,
            error.status === 'warning' && (
              <Button
                key="refresh"
                onClick={() => window.location.reload()}
              >
                Попробовать снова
              </Button>
            )
          ]}
        />
      </div>
    );
  }

  if (result) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Title level={2}>{result.title}</Title>
        <Paragraph>{result.message}</Paragraph>
        <Button
          type="primary"
          onClick={() => navigate('/')}
        >
          На главную
        </Button>
      </div>
    );
  }

  return null;
};

export default JoinGroupMenu;