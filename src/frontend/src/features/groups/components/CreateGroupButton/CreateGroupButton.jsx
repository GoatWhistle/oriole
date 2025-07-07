import React, { useState, useEffect } from 'react';
import { Button, Modal, Form, Input } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

import { fetchCheckAuth } from '../../../api/check_auth.jsx';
import { handleCreateGroup } from '../../handlers/group.jsx';

import styles from './CreateGroupButton.module.css';

const CreateGroupButton = () => {
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const authStatus = await fetchCheckAuth();
      setIsAuthenticated(authStatus);
      setLoading(false);
    };

    checkAuth();
  }, []);

  const showModal = () => {
    setOpen(true);
  };

  const handleCancel = () => {
    form.resetFields();
    setOpen(false);
  };

  const onFinish = async (values) => {
    const createdGroup = await handleCreateGroup(values, setConfirmLoading, form, setOpen);
  };

  if (loading) {
    return null;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className={styles.container}>
      <Button type="primary" onClick={showModal} className={styles.createButton}>
          <PlusOutlined />
          Создать группу
      </Button>
      <Modal
        title="Новая группа"
        open={open}
        onOk={form.submit}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        okText="Создать"
        cancelText="Отмена"
        className={styles.modal}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            label="Название группы"
            name="title"
            rules={[{ required: true, message: 'Пожалуйста, введите название группы' }]}
          >
            <Input placeholder="Введите название группы" className={styles.input} />
          </Form.Item>

          <Form.Item
            label="Описание (необязательно)"
            name="description"
            initialValue=""
          >
            <Input.TextArea rows={4} placeholder="Введите описание группы" className={styles.textarea} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CreateGroupButton;
