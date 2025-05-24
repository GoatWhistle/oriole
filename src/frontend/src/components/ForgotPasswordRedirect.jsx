import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Input, Button, message, Card, Typography } from 'antd';
import axios from 'axios';

const { Title } = Typography;

const ForgotPasswordRedirect = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    const { newPassword, confirmPassword } = values;

    if (newPassword !== confirmPassword) {
      message.error('Пароли не совпадают');
      return;
    }

    try {
      setLoading(true);

      const response = await axios.get(
        `/api/v1/verify/forgot_password_redirect/${token}`,
        {
          params: { new_password: newPassword },
          withCredentials: true
        }
      );

      if (response.data.status === 'success') {
        message.success(response.data.message || 'Пароль успешно изменен');
        navigate('/');
      } else {
        throw new Error(response.data.message || 'Не удалось изменить пароль');
      }
    } catch (error) {
      console.error('Ошибка смены пароля:', error);

      if (error.response) {
        if (error.response.status === 403) {
          message.error('Новый пароль должен отличаться от предыдущего');
        } else if (error.response.status === 400) {
          message.error(error.response.data.detail || 'Неверный запрос');
        } else {
          message.error('Ошибка сервера');
        }
      } else {
        message.error('Ошибка сети');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: '#f0f2f5'
    }}>
      <Card style={{ width: 450 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>
          Восстановление пароля
        </Title>

        <Form
          form={form}
          name="forgotPassword"
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            name="newPassword"
            label="Новый пароль"
            rules={[
              { required: true, message: 'Пожалуйста, введите новый пароль!' },
              { min: 8, message: 'Пароль должен содержать минимум 8 символов' }
            ]}
          >
            <Input.Password placeholder="Введите новый пароль" size="large" />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            label="Подтвердите пароль"
            dependencies={['newPassword']}
            rules={[
              { required: true, message: 'Пожалуйста, подтвердите пароль!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('newPassword') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Пароли не совпадают!'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="Подтвердите пароль" size="large" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
            >
              Сохранить
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default ForgotPasswordRedirect;