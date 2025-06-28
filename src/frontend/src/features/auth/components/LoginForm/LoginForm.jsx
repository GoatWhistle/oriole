import React, { useState } from 'react';
import { Button, Form, Input, Typography, Divider, Row, Col } from 'antd';
import { Link, useNavigate } from 'react-router-dom';

import { handleLogin, handleForgotPassword } from '../../handlers/user.jsx';

import styles from './LoginForm.module.css';

const { Title } = Typography;

const LoginForm = () => {
  const [loading, setLoading] = useState(false);
  const [forgotPasswordLoading, setForgotPasswordLoading] = useState(false);
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    await handleLogin(values, navigate, setLoading);
  };

  const onForgotPassword = async () => {
    const email = form.getFieldValue('email');
    await handleForgotPassword(email, setForgotPasswordLoading);
  };

  return (
    <div className={styles.container}>
      <div className={styles.formContainer}>
        <Title level={2} className={styles.title}>Вход в систему</Title>

        <Form
          form={form}
          name="login"
          onFinish={onFinish}
          layout="vertical"
          className={styles.form}
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
                <Button
                  type="link"
                  onClick={onForgotPassword}
                  loading={forgotPasswordLoading}
                  className={styles.forgotPassword}
                >
                  {forgotPasswordLoading ? 'Отправка...' : 'Забыли пароль?'}
                </Button>
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
              className={styles.submitButton}
            >
              Войти
            </Button>
          </Form.Item>

          <Divider plain className={styles.divider}>Еще нет аккаунта?</Divider>

          <Row justify="center" className={styles.registerRow}>
            <Col>
              <Link to="/registration" className={styles.registerLink}>Зарегистрироваться</Link>
            </Col>
          </Row>
        </Form>
      </div>
    </div>
  );
};

export default LoginForm;