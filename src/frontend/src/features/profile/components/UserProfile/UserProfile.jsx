import React, { useState, useEffect } from 'react';
import {
  Card,
  Button,
  Form,
  Input,
  Typography,
  Divider,
  Spin,
  Modal,
  Popconfirm
} from 'antd';
import { ExclamationCircleFilled, CloseOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import { handleShowUserProfile,
         handleUpdateProfile,
         handleResetPassword,
         handleLogout,
         handleDeleteAccount
} from '../../handlers/user.jsx';

import styles from './UserProfile.module.css';

const { Title, Text } = Typography;

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [resetLoading, setResetLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    handleShowUserProfile(setUser, setLoading);
  }, []);

  const handleEdit = () => {
    form.setFieldsValue({
      name: user.profile.name,
      surname: user.profile.surname,
      patronymic: user.profile.patronymic
    });
    setEditing(true);
  };

  const handleSave = async () => {
    const values = await form.validateFields();
    const success = await handleUpdateProfile(values, setUser);
    if (success) {
      setEditing(false);
      window.location.reload();
    }
  };

  const handleCancel = () => {
    setEditing(false);
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" />
      </div>
    );
  }

  if (!user) {
    return <div className={styles.errorContainer}>Пользователь не найден</div>;
  }

  return (
    <div className={styles.container}>
      <Card
        title={
          <Title level={2} className={styles.title}>
            Профиль пользователя
          </Title>
        }
        bordered={false}
        className={styles.card}
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

            <div className={styles.formActions}>
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
            <div className={styles.field}>
              <Text strong className={styles.fieldLabel}>ID:</Text>
              <Text className={styles.fieldValue}>{user.profile.user_id}</Text>
            </div>

            <div className={styles.emailContainer}>
              <div className={styles.field}>
                <Text strong className={styles.fieldLabel}>Email:</Text>
                <Text className={styles.fieldValue}>{user.email}</Text>
              </div>
              <Button
                type="link"
                onClick={() => handleResetPassword(setResetLoading)}
                loading={resetLoading}
                className={styles.resetPasswordButton}
              >
                Сбросить пароль
              </Button>
            </div>

            <Divider />

            <div className={styles.profileGrid}>
              <div className={styles.profileField}>
                <Text strong className={styles.profileLabel}>Имя</Text>
                <Text className={styles.profileValue}>{user.profile.name}</Text>
              </div>

              <div className={styles.profileField}>
                <Text strong className={styles.profileLabel}>Фамилия</Text>
                <Text className={styles.profileValue}>{user.profile.surname}</Text>
              </div>

              <div className={styles.profileField}>
                <Text strong className={styles.profileLabel}>Отчество</Text>
                <Text className={styles.profileValue}>{user.profile.patronymic || '—'}</Text>
              </div>
            </div>

            <div className={styles.actions}>
              <Button type="primary" onClick={handleEdit}>
                Редактировать профиль
              </Button>
              <Popconfirm
                title="Вы уверены, что хотите удалить аккаунт? Это действие нельзя отменить!"
                onConfirm={() => handleDeleteAccount(navigate)}
                okText="Да, удалить"
                cancelText="Отмена"
                okButtonProps={{ danger: true }}
              >
                <Button danger icon={<CloseOutlined />} className={styles.deleteButton}>
                  Удалить аккаунт
                </Button>
              </Popconfirm>
              <Button onClick={() => handleLogout(navigate)} className={styles.logoutButton}>
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