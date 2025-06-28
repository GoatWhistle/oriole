import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Typography } from 'antd';

import { handleForgotPassword } from '../../handlers/user.jsx';

import styles from './ForgotPasswordRedirect.module.css';

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
    await handleForgotPassword(token, newPassword, navigate, setLoading);
  };

  return (
    <div className={styles.container}>
      <Card className={styles.card}>
        <Title level={2} className={styles.title}>
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
              className={styles.submitButton}
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