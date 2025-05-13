import React, { useState } from 'react';
import { Button, Form, Input, message, Typography, Divider, Row, Col } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Title, Text } = Typography;

const LoginForm = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', values.email);
      formData.append('password', values.password);
      formData.append('grant_type', 'password');

      const response = await axios.post('http://localhost:8000/api/v1/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
      });

      localStorage.setItem('access_token', response.data.access_token);
      message.success('Вход выполнен успешно!');
      navigate('/');

    } catch (error) {
      console.error('Ошибка входа:', error);

      if (error.response) {
        switch (error.response.status) {
          case 401:
            message.error('Неверный email или пароль');
            break;
          case 404:
            message.error('Пользователь не найден');
            break;
          default:
            message.error(`Ошибка сервера: ${error.response.status}`);
        }
      } else {
        message.error('Ошибка сети. Проверьте подключение');
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
      <div style={{
        background: '#fff',
        padding: '32px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        width: '400px'
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Вход в систему</Title>

        <Form
          name="login"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: 'Введите ваш email!' },
              { type: 'email', message: 'Неверный формат email' }
            ]}
          >
            <Input placeholder="example@mail.com" size="large" />
          </Form.Item>

          <Form.Item
            label="Пароль"
            name="password"
            rules={[{ required: true, message: 'Введите пароль!' }]}
          >
            <Input.Password placeholder="Ваш пароль" size="large" />
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

          <Divider plain>или</Divider>

          <Row justify="center" style={{ marginTop: 16 }}>
            <Col>
              <Text>Нет аккаунта? </Text>
              <Link to="/registration" style={{ fontWeight: 500 }}>Зарегистрируйтесь</Link>
            </Col>
          </Row>
        </Form>
      </div>
    </div>
  );
};

export default LoginForm;