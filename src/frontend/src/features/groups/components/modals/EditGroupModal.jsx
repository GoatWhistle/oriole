import React from 'react';
import { Modal, Form, Input } from 'antd';

const { TextArea } = Input;

export const EditGroupModal = ({ visible, group, onCancel, onSave }) => {
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      onSave(values);
    } catch (err) {
      console.error('Validation failed:', err);
    }
  };

  return (
    <Modal
      title="Редактирование группы"
      visible={visible}
      onOk={handleSubmit}
      onCancel={onCancel}
      okText="Сохранить"
      cancelText="Отмена"
      afterClose={() => form.resetFields()}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          title: group?.title,
          description: group?.description
        }}
      >
        <Form.Item
          name="title"
          label="Название группы"
          rules={[{ required: true, message: 'Пожалуйста, введите название группы' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="description"
          label="Описание группы"
        >
          <TextArea rows={4} />
        </Form.Item>
      </Form>
    </Modal>
  );
};
