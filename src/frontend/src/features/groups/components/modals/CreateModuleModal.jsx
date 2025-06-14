import React from 'react';
import { Modal, Form, Input, Switch, DatePicker, Typography } from 'antd';
import dayjs from 'dayjs';

const { TextArea } = Input;
const { RangePicker } = DatePicker;
const { Text } = Typography;

export const CreateModuleModal = ({ visible, onCancel, onCreate }) => {
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      onCreate(values);
    } catch (err) {
      console.error('Validation failed:', err);
    }
  };

  const disabledDate = (current) => {
    return current && current < dayjs().startOf('day');
  };

  return (
    <Modal
      title="Создание нового модуля"
      visible={visible}
      onOk={handleSubmit}
      onCancel={onCancel}
      okText="Создать"
      cancelText="Отмена"
      width={700}
      afterClose={() => form.resetFields()}
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="title"
          label="Название модуля"
          rules={[{ required: true, message: 'Пожалуйста, введите название модуля' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          name="description"
          label="Описание модуля"
        >
          <TextArea rows={4} />
        </Form.Item>
        <Form.Item
          name="is_contest"
          label="Это контест?"
          valuePropName="checked"
        >
          <Switch />
        </Form.Item>
        <Form.Item
          name="dateRange"
          label="Период активности"
          rules={[{ required: true, message: 'Пожалуйста, выберите период активности' }]}
        >
          <RangePicker
            showTime={false}
            format="YYYY-MM-DD HH:mm:ss"
            disabledDate={disabledDate}
            style={{ width: '100%' }}
          />
        </Form.Item>
        <Text type="secondary">Модуль станет доступен участникам в указанный период времени</Text>
      </Form>
    </Modal>
  );
};
