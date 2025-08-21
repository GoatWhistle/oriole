import React, { useEffect, useState } from 'react';
import { Modal, Form, Input, Checkbox, DatePicker } from 'antd';
import dayjs from 'dayjs';
import { handleUpdateModule } from '../../../handlers/module.jsx';
import styles from './EditModuleModal.module.css';

const { TextArea } = Input;

const EditModuleModal = ({
  visible,
  onCancel,
  module,
  onModuleUpdated
}) => {
  const [form] = Form.useForm();
  const [confirmLoading, setConfirmLoading] = useState(false);

  useEffect(() => {
    if (visible && module) {
      form.setFieldsValue({
        title: module.title,
        description: module.description,
        is_contest: module.is_contest,
        dateRange: [
          dayjs(module.start_datetime),
          dayjs(module.end_datetime)
        ]
      });
    }
  }, [visible, module, form]);

  const handleSubmit = async (values) => {
    try {
      setConfirmLoading(true);
      const updatedModule = await handleUpdateModule(module.id, {
        ...values,
        start_datetime: values.dateRange[0].toISOString(),
        end_datetime: values.dateRange[1].toISOString()
      });
      onModuleUpdated(updatedModule);
      onCancel();
    } catch (error) {
      console.error('Ошибка при обновлении модуля:', error);
    } finally {
      setConfirmLoading(false);
    }
  };

  return (
    <Modal
      title="Редактирование модуля"
      visible={visible}
      onCancel={onCancel}
      onOk={() => form.submit()}
      okText="Сохранить"
      cancelText="Отмена"
      confirmLoading={confirmLoading}
      className={styles.modal}
      width={700}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        className={styles.form}
      >
        <Form.Item
          name="title"
          label="Название модуля"
          rules={[
            { required: true, message: 'Введите название модуля' },
            { max: 100, message: 'Максимальная длина 100 символов' }
          ]}
        >
          <Input placeholder="Введите название модуля" />
        </Form.Item>

        <Form.Item
          name="description"
          label="Описание модуля"
          rules={[
            { required: true, message: 'Введите описание модуля' },
            { max: 1000, message: 'Максимальная длина 1000 символов' }
          ]}
        >
          <TextArea rows={4} placeholder="Опишите модуль подробно" />
        </Form.Item>

        <Form.Item
          name="is_contest"
          label="Тип модуля"
          valuePropName="checked"
        >
          <Checkbox>Контест</Checkbox>
        </Form.Item>

        <Form.Item
          name="dateRange"
          label="Срок выполнения"
          rules={[{ required: true, message: 'Укажите срок выполнения' }]}
        >
          <DatePicker.RangePicker
            showTime
            format="DD.MM.YYYY HH:mm"
            style={{ width: '100%' }}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default EditModuleModal;
