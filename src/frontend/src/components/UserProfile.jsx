import React, { useState, useEffect } from 'react';
import {
  Card,
  Button,
  Form,
  Input,
  Typography,
  Divider,
  message,
  Spin,
  Modal,
  Popconfirm
} from 'antd';
import { ExclamationCircleFilled, CloseOutlined } from '@ant-design/icons';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const { Title, Text } = Typography;
const { confirm } = Modal;

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [resetLoading, setResetLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('/api/v1/auth/check-auth', {
          withCredentials: true
        });
        setUser(response.data);
      } catch (error) {
        message.error('Ошибка загрузки профиля');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleResetPassword = async () => {
    try {
      setResetLoading(true);
      const response = await axios.post(
        '/api/v1/auth/reset_password',
        {},
        { withCredentials: true }
      );

      message.success(response.data.message || 'Ссылка для сброса пароля отправлена на ваш email');
    } catch (error) {
      console.error('Ошибка при запросе сброса пароля:', error);
      message.error(error.response?.data?.detail || 'Не удалось отправить ссылку для сброса пароля');
    } finally {
      setResetLoading(false);
    }
  };

  const handleEdit = () => {
    form.setFieldsValue({
      name: user.profile.name,
      surname: user.profile.surname,
      patronymic: user.profile.patronymic
    });
    setEditing(true);
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      const updatedData = {
        name: values.name,
        surname: values.surname,
        patronymic: values.patronymic,
      };

      const response = await axios.patch(
        `/api/v1/users/profile`,
        updatedData,
        { withCredentials: true }
      );

      setUser(response.data);
      setEditing(false);
      window.location.reload();
      message.success('Профиль успешно обновлен!');
    } catch (error) {
      message.error('Ошибка при обновлении профиля');
      console.error(error);
    }
  };

  const handleCancel = () => {
    setEditing(false);
  };

  const handleLogout = async () => {
    try {
      await axios.delete('/api/v1/auth/logout', { withCredentials: true });
      message.success('Вы успешно вышли из системы');
      navigate('/');
    } catch (error) {
      message.error('Ошибка при выходе из системы');
      console.error(error);
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await axios.delete('/api/v1/users', {
        withCredentials: true
      });
      message.success('Аккаунт успешно удален');
      navigate('/');
    } catch (error) {
      message.error('Произошла ошибка при удалении аккаунта');
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!user) {
    return <div>Пользователь не найден</div>;
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '24px' }}>
      <Card
        title={
          <Title level={2} style={{ marginBottom: 0 }}>
            Профиль пользователя
          </Title>
        }
        bordered={false}
        style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
      >
        {editing ? (
          <Form form={form} layout="vertical">
            <Form.Item
              label="Имя"
              name="name"
              rules={[{ required: true, message: 'Введите имя' }]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Фамилия"
              name="surname"
              rules={[{ required: true, message: 'Введите фамилию' }]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Отчество"
              name="patronymic"
            >
              <Input />
            </Form.Item>

            <div style={{ display: 'flex', gap: '16px', marginTop: '24px' }}>
              <Button type="primary" onClick={handleSave}>
                Сохранить изменения
              </Button>
              <Button onClick={handleCancel}>
                Отмена
              </Button>
            </div>
          </Form>
        ) : (
          <>
            <div style={{ marginBottom: '24px' }}>
              <Text strong style={{ fontSize: '16px' }}>ID:</Text>
              <Text style={{ marginLeft: '8px' }}>{user.profile.user_id}</Text>
            </div>

            <div style={{ marginBottom: '24px', display: 'flex', alignItems: 'center' }}>
              <div style={{ flex: 1 }}>
                <Text strong style={{ fontSize: '16px' }}>Email:</Text>
                <Text style={{ marginLeft: '8px' }}>{user.email}</Text>
              </div>
              <Button
                type="link"
                onClick={handleResetPassword}
                loading={resetLoading}
                style={{ padding: 0 }}
              >
                Сбросить пароль
              </Button>
            </div>

            <Divider />

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px' }}>
              <div>
                <Text strong style={{ display: 'block', marginBottom: '8px' }}>Имя</Text>
                <Text>{user.profile.name}</Text>
              </div>

              <div>
                <Text strong style={{ display: 'block', marginBottom: '8px' }}>Фамилия</Text>
                <Text>{user.profile.surname}</Text>
              </div>

              <div>
                <Text strong style={{ display: 'block', marginBottom: '8px' }}>Отчество</Text>
                <Text>{user.profile.patronymic || '—'}</Text>
              </div>
            </div>

            <div style={{ marginTop: '32px', textAlign: 'right' }}>
              <Button type="primary" onClick={handleEdit}>
                Редактировать профиль
              </Button>
              <Popconfirm
                title={`Вы уверены, что хотите удалить аккаунт? Это действие нельзя отменить!`}
                onConfirm={handleDeleteAccount}
                okText="Да, удалить"
                cancelText="Отмена"
                okButtonProps={{ danger: true }}
              >
                <Button danger icon={<CloseOutlined />} style={{ marginLeft: '16px' }}>
                  Удалить аккаунт
                </Button>
              </Popconfirm>
              <Button onClick={handleLogout} style={{ marginLeft: '16px' }}>
                Выйти
              </Button>
            </div>
          </>
        )}
      </Card>
    </div>
  );
};

export default UserProfile;