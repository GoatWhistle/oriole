import React from 'react';
import { Modal, Input, Button, Typography, Alert } from 'antd';
import { CopyOutlined, ClockCircleOutlined } from '@ant-design/icons';

const { Text } = Typography;

export const InviteLinkModal = ({ visible, inviteLink, expiryTime, onCancel, onCopy }) => {
  return (
    <Modal
      title="Ссылка для вступления в группу"
      visible={visible}
      onCancel={onCancel}
      footer={[
        <Button
          key="copy"
          icon={<CopyOutlined />}
          onClick={onCopy}
          type="primary"
        >
          Скопировать ссылку
        </Button>,
        <Button key="close" onClick={onCancel}>
          Закрыть
        </Button>
      ]}
    >
      <Input
        value={inviteLink || 'Генерация ссылки...'}
        readOnly
        addonBefore="Ссылка:"
        style={{ marginBottom: 16 }}
      />
      <div style={{ display: 'flex', alignItems: 'center', color: 'rgba(0, 0, 0, 0.45)' }}>
        <ClockCircleOutlined style={{ marginRight: 8 }} />
        <Text type="secondary">
          Ссылка действительна до: {expiryTime ? expiryTime.toLocaleString() : 'неизвестно'}
        </Text>
      </div>
      <Alert
        message="Инструкция"
        description="Отправьте эту ссылку пользователям, которых вы хотите добавить в группу."
        type="info"
        showIcon
        style={{ marginTop: 16 }}
      />
    </Modal>
  );
};
