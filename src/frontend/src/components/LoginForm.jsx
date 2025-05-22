import React, { useState } from 'react';
import { Button, Form, Input, message, Typography, Divider, Row, Col } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Title } = Typography;

const LoginForm = () => {
  const [loading, setLoading] = useState(false);
  const [forgotPasswordLoading, setForgotPasswordLoading] = useState(false);
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', values.email);
      formData.append('password', values.password);

      const response = await axios.post('/api/v1/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        navigate('/');
      } else {
        throw new Error('Токен не получен');
      }

    } catch (error) {
      console.error('Ошибка входа:', error);
      if (error.response) {
        if (error.response.status === 400 || error.response.status === 401) {
          message.error('Неверный email или пароль');
        } else if (error.response.status === 422) {
          message.error('Ошибка валидации данных');
        } else {
          message.error(`Ошибка сервера: ${error.response.status}`);
        }
      } else {
        message.error('Ошибка сети или сервера');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    const email = form.getFieldValue('email');
    if (!email) {
      message.error('Пожалуйста, введите ваш email для восстановления пароля');
      return;
    }

    setForgotPasswordLoading(true);
    try {
      const response = await axios.post('/api/v1/auth/forgot_password', { email });
      message.success(response.data.message || 'Инструкции по восстановлению пароля отправлены на ваш email');
    } catch (error) {
      console.error('Ошибка восстановления пароля:', error);
      if (error.response) {
        if (error.response.status === 404) {
          message.error('Пользователь с таким email не найден');
        } else {
          message.error(`Ошибка: ${error.response.data.detail || 'Неизвестная ошибка сервера'}`);
        }
      } else {
        message.error('Ошибка сети или сервера');
      }
    } finally {
      setForgotPasswordLoading(false);
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
      <div style={{
        background: '#fff',
        padding: '32px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        width: '450px'
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Вход в систему</Title>

        <Form
          form={form}
          name="login"
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: 'Пожалуйста, введите ваш email!' },
              { type: 'email', message: 'Введите корректный email адрес' },
            ]}
          >
            <Input placeholder="example@mail.com" size="large" />
          </Form.Item>

          <Form.Item
            label="Пароль"
            name="password"
            rules={[
              { required: true, message: 'Пожалуйста, введите пароль!' },
            ]}
          >
            <Input.Password placeholder="Введите пароль" size="large" />
          </Form.Item>

          <Form.Item>
            <Row justify="space-between" align="middle">
              <Col>
                <a onClick={handleForgotPassword} disabled={forgotPasswordLoading}>
                  {forgotPasswordLoading ? 'Отправка...' : 'Забыли пароль?'}
                </a>
              </Col>
            </Row>
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
            >
              Войти
            </Button>
          </Form.Item>

          <Divider plain>Еще нет аккаунта?</Divider>

          <Row justify="center" style={{ marginTop: 16 }}>
            <Col>
              <Link to="/registration" style={{ fontWeight: 500 }}>Зарегистрироваться</Link>
            </Col>
          </Row>
        </Form>
      </div>
    </div>
  );
};

export default LoginForm;