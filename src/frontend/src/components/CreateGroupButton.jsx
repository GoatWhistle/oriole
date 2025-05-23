import React, { useState } from 'react';
import { Button, Modal, Form, Input, message } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateGroupButton = () => {
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

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
      const response = await axios.post('api/v1/groups/', values, {
        withCredentials: true,
      });

      message.success(`Группа "${response.data.title}" успешно создана!`);
      form.resetFields();
      setOpen(false);

      // Здесь можно добавить обновление списка групп или другие действия после успешного создания
    } catch (error) {
      console.error('Ошибка при создании группы:', error);
      message.error('Не удалось создать группу');
    } finally {
      setConfirmLoading(false);
      window.location.reload();
    }
  };

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
          >
            <Input.TextArea rows={4} placeholder="Введите описание группы" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default CreateGroupButton;