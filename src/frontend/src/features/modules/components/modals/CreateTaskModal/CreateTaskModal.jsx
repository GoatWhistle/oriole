import React, { useState } from 'react';
import { Modal, Form, Input, InputNumber, DatePicker } from 'antd';
import dayjs from 'dayjs';
import { handleCreateTask } from '../../../handlers/module.jsx';
import styles from './CreateTaskModal.module.css';

const { TextArea } = Input;

const CreateTaskModal = ({
  visible,
  onCancel,
  moduleId,
  module,
  onTaskCreated,
  navigate
}) => {
  const [form] = Form.useForm();
  const [confirmLoading, setConfirmLoading] = useState(false);

  const disabledDateForTask = (current) => {
    const moduleStart = dayjs(module.start_datetime);
    const moduleEnd = dayjs(module.end_datetime);
    return current && (
      current < moduleStart.startOf('day') ||
      current > moduleEnd.endOf('day')
    );
  };

  const handleSubmit = async (values) => {
    try {
      setConfirmLoading(true);
      await handleCreateTask({
        ...values,
        module_id: parseInt(moduleId),
        start_datetime: values.dateRange[0].toISOString(),
        end_datetime: values.dateRange[1].toISOString()
      }, moduleId, navigate, onTaskCreated);
      onCancel();
    } catch (error) {
      console.error('Ошибка при создании задания:', error);
    } finally {
      setConfirmLoading(false);
    }
  };

  return (
    <Modal
      title="Создание нового задания"
      visible={visible}
      onCancel={onCancel}
      onOk={() => form.submit()}
      okText="Создать"
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
          label="Название задания"
          rules={[
            { required: true, message: 'Введите название задания' },
            { max: 100, message: 'Максимальная длина 100 символов' }
          ]}
        >
          <Input placeholder="Введите название задания" />
        </Form.Item>

        <Form.Item
          name="description"
          label="Описание задания"
          rules={[
            { required: true, message: 'Введите описание задания' },
            { max: 1000, message: 'Максимальная длина 1000 символов' }
          ]}
        >
          <TextArea rows={4} placeholder="Опишите задание подробно" />
        </Form.Item>

        <Form.Item
          name="correct_answer"
          label="Правильный ответ"
          rules={[
            { required: true, message: 'Введите правильный ответ' },
            { max: 500, message: 'Максимальная длина 500 символов' }
          ]}
        >
          <Input placeholder="Введите правильный ответ" />
        </Form.Item>

        <Form.Item
          name="max_attempts"
          label="Максимальное количество попыток"
          rules={[
            { required: true, message: 'Укажите количество попыток' },
            { type: 'number', min: 1, max: 100, message: 'Допустимые значения от 1 до 100' }
          ]}
        >
          <InputNumber min={1} max={100} style={{ width: '100%' }} />
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
            disabledDate={disabledDateForTask}
            ranges={{
              'Весь модуль': [
                dayjs(module.start_datetime),
                dayjs(module.end_datetime)
              ]
            }}
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default CreateTaskModal;