import React, { useState, useEffect } from 'react';
import { Card, Button, Form, Input, Typography, Divider, message, Spin } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const { Title, Text } = Typography;

const UserProfile = () => {
  const [user, setUser ] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('/api/v1/check-auth', {
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

  const handleEdit = () => {
    form.setFieldsValue({
      email: user.email,
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
        email: values.email,
        profile: {
          name: values.name,
          surname: values.surname,
          patronymic: values.patronymic
        }
      };
      const response = await axios.patch(
        `/api/v1/users/${user.profile.user_id}`,
        updatedData,
        { withCredentials: true }
      );

      setUser (response.data);
      setEditing(false);
      message.success('Профиль успешно обновлен!');
      navigate('/user-profile'); // Перенаправление на страницу профиля
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
      await axios.delete('/api/v1/logout', { withCredentials: true });
      message.success('Вы успешно вышли из системы');
      navigate('/'); // Перенаправление на страницу входа
    } catch (error) {
      message.error('Ошибка при выходе из системы');
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
              label="Email"
              name="email"
              rules={[
                { required: true, message: 'Введите email' },
                { type: 'email', message: 'Некорректный email' }
              ]}
            >
              <Input />
            </Form.Item>

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

            <div style={{ marginBottom: '24px' }}>
              <Text strong style={{ fontSize: '16px' }}>Email:</Text>
              <Text style={{ marginLeft: '8px' }}>{user.email}</Text>
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
              <Button type="danger" onClick={handleLogout} style={{ marginLeft: '16px' }}>
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
