import React, { useState } from 'react';
import { Button, Form, Input, message, Typography, Divider, Row, Col } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Title, Text } = Typography;

const RegistrationForm = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const userData = {
        email: values.email,
        password: values.password, // Изменено на 'password' вместо 'hashed_password'
        name: values.firstName,
        surname: values.lastName,
        patronymic: values.middleName || null,
        is_active: true,
        is_superuser: false,
        is_verified: false
      };

      const response = await axios.post('http://localhost:8000/api/v1/register', userData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });

      message.success('Регистрация прошла успешно!');
      navigate('/login');

    } catch (error) {
      console.error('Ошибка регистрации:', error);

      if (error.response) {
        if (error.response.status === 400) {
          message.error('Пользователь с таким email уже существует');
        } else if (error.response.status === 422) {
          const errors = error.response.data.detail;
          if (Array.isArray(errors)) {
            errors.forEach(err => {
              message.error(`${err.loc[1]}: ${err.msg}`);
            });
          } else {
            message.error('Ошибка валидации данных');
          }
        } else {
          message.error(`Ошибка сервера: ${error.response.status}`);
        }
      } else if (error.code === "ERR_NETWORK") {
        message.error('Проблема с соединением. Проверьте: \n1. Запущен ли бэкенд\n2. Настройки CORS\n3. Сетевые ограничения');
      } else {
        message.error('Неизвестная ошибка при регистрации');
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
        width: '450px'
      }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>Регистрация</Title>

        <Form
          form={form}
          name="register"
          onFinish={onFinish}
          layout="vertical"
          scrollToFirstError
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="Имя"
                name="firstName"
                rules={[
                  { required: true, message: 'Пожалуйста, введите ваше имя!' },
                  { max: 31, message: 'Имя не должно превышать 31 символ' }
                ]}
              >
                <Input placeholder="Иван" size="large" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="Фамилия"
                name="lastName"
                rules={[
                  { required: true, message: 'Пожалуйста, введите вашу фамилию!' },
                  { max: 31, message: 'Фамилия не должна превышать 31 символ' }
                ]}
              >
                <Input placeholder="Иванов" size="large" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            label="Отчество"
            name="middleName"
            rules={[
              { max: 63, message: 'Отчество не должно превышать 63 символа' }
            ]}
          >
            <Input placeholder="Иванович (необязательно)" size="large" />
          </Form.Item>

          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: 'Пожалуйста, введите ваш email!' },
              { type: 'email', message: 'Введите корректный email адрес' },
              { max: 63, message: 'Email не должен превышать 63 символа' }
            ]}
          >
            <Input placeholder="example@mail.com" size="large" />
          </Form.Item>

          <Form.Item
            label="Пароль"
            name="password"
            rules={[
              { required: true, message: 'Пожалуйста, введите пароль!' },
              { min: 8, message: 'Пароль должен быть не менее 8 символов' },
              { max: 1023, message: 'Пароль не должен превышать 1023 символа' },
              { pattern: /[A-Z]/, message: 'Пароль должен содержать хотя бы одну заглавную букву' },
              { pattern: /[0-9]/, message: 'Пароль должен содержать хотя бы одну цифру' }
            ]}
            hasFeedback
          >
            <Input.Password placeholder="Придумайте пароль" size="large" />
          </Form.Item>

          <Form.Item
            label="Подтвердите пароль"
            name="confirmPassword"
            dependencies={['password']}
            hasFeedback
            rules={[
              { required: true, message: 'Пожалуйста, подтвердите пароль!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Пароли не совпадают!'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="Повторите пароль" size="large" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              size="large"
            >
              Зарегистрироваться
            </Button>
          </Form.Item>

          <Divider plain>Уже есть аккаунт?</Divider>

          <Row justify="center" style={{ marginTop: 16 }}>
            <Col>
              <Link to="/login" style={{ fontWeight: 500 }}>Войти в систему</Link>
            </Col>
          </Row>
        </Form>
      </div>
    </div>
  );
};

export default RegistrationForm;
