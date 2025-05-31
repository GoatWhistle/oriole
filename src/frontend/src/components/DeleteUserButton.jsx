import React, { useState } from 'react';
import { Button, Modal, message } from 'antd';
import { ExclamationCircleFilled } from '@ant-design/icons';
import axios from 'axios';

const DeleteUserButton = () => {
  const [loading, setLoading] = useState(false);
  const { confirm } = Modal;

  const showDeleteConfirm = () => {
    confirm({
      title: 'Вы уверены, что хотите удалить свой аккаунт?',
      icon: <ExclamationCircleFilled />,
      content: 'Это действие нельзя отменить. Все ваши данные будут безвозвратно удалены.',
      okText: 'Да, удалить',
      okType: 'danger',
      cancelText: 'Отмена',
      onOk() {
        return handleDelete();
      },
      onCancel() {
        console.log('Отмена удаления');
      },
    });
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      const response = await axios.delete('/api/v1/users/', {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 204) {
        message.success('Ваш аккаунт успешно удален');

        setTimeout(() => {
          window.location.href = '/login';
        }, 1000);
      } else {
        throw new Error(`Неожиданный статус ответа: ${response.status}`);
      }

    } catch (error) {
      console.error('Ошибка при удалении аккаунта:', error);

      if (axios.isAxiosError(error)) {
        if (error.response) {
          switch (error.response.status) {
            case 401:
              message.error('Требуется авторизация');
              break;
            case 403:
              message.error('Недостаточно прав');
              break;
            default:
              message.error('Произошла ошибка при удалении аккаунта');
          }
        } else if (error.request) {
          message.error('Не получен ответ от сервера');
        } else {
          message.error('Ошибка при настройке запроса');
        }
      } else {
        message.error('Неизвестная ошибка');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      type="primary"
      danger
      onClick={showDeleteConfirm}
      loading={loading}
    >
      Удалить аккаунт
    </Button>
  );
};

export default DeleteUserButton;