import React, { useState } from 'react';
import { Modal, Form, InputNumber, Select, Alert } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Option } = Select;

export const InviteSettingsModal = ({ visible, onCancel, onGenerate }) => {
  const [form] = Form.useForm();
  const [inviteType, setInviteType] = useState('single_use');
  const [expiresMinutes, setExpiresMinutes] = useState(30);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      onGenerate({
        expiresMinutes: values.expiresMinutes,
        inviteType: values.inviteType
      });
    } catch (err) {
      console.error('Validation failed:', err);
    }
  };

  return (
    <Modal
      title="Настройки приглашения"
      visible={visible}
      onOk={handleSubmit}
      onCancel={onCancel}
      okText="Сгенерировать ссылку"
      cancelText="Отмена"
    >
      <Form form={form} layout="vertical" initialValues={{ inviteType, expiresMinutes }}>
        <Form.Item name="inviteType" label="Тип приглашения">
          <Select onChange={setInviteType}>
            <Option value="single_use">Одноразовое</Option>
            <Option value="multi_use">Многоразовое</Option>
          </Select>
        </Form.Item>
        <Form.Item
          name="expiresMinutes"
          label="Срок действия (минуты)"
          rules={[{ required: true, message: 'Укажите срок действия' }]}
        >
          <InputNumber
            min={5}
            max={10080}
            style={{ width: '100%' }}
          />
        </Form.Item>
        <Alert
          message="Информация"
          description="Ссылка будет действительна только в течение указанного времени."
          type="info"
          showIcon
          icon={<InfoCircleOutlined />}
        />
      </Form>
    </Modal>
  );
};
