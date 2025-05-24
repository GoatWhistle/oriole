import React, { useState, useEffect } from 'react';
import { Button, Modal, Form, Input, message } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateGroupButton = () => {
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loadingAuthCheck, setLoadingAuthCheck] = useState(true);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await axios.get('api/v1/auth/check-auth', {
          withCredentials: true,
        });
        setIsAuthenticated(true);
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setLoadingAuthCheck(false);
      }
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
    setConfirmLoading(true);
    try {
      // Явно устанавливаем пустую строку, если description отсутствует или undefined
      const groupData = {
        title: values.title,
        description: values.description || '',
      };

      const response = await axios.post('api/v1/groups/', groupData, {
        withCredentials: true,
      });

      message.success(`Группа "${response.data.title}" успешно создана!`);
      form.resetFields();
      setOpen(false);

    } catch (error) {
      console.error('Ошибка при создании группы:', error);
      message.error('Не удалось создать группу');
    } finally {
      setConfirmLoading(false);
      window.location.reload();
    }
  };

  if (loadingAuthCheck) {
    return null;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      <Button type="primary" onClick={showModal}>
        Создать группу
      </Button>
      <Modal
        title="Создание новой группы"
        open={open}
        onOk={form.submit}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        okText="Создать"
        cancelText="Отмена"
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
            <Input placeholder="Введите название группы" />
          </Form.Item>

          <Form.Item
            label="Описание (необязательно)"
            name="description"
            initialValue="" // Явно устанавливаем начальное значение как пустую строку
          >
            <Input.TextArea rows={4} placeholder="Введите описание группы" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default CreateGroupButton;