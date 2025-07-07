import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Divider,
  Button,
  Space,
  Form,
  Input,
  InputNumber,
  Alert,
  Statistic,
  Row,
  Col,
  Modal,
  Popconfirm,
  DatePicker,
  Spin
} from 'antd';
import {
  CheckOutlined,
  CloseOutlined,
  EditOutlined,
  ClockCircleOutlined,
  ArrowLeftOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';
import {
  handleGetTask,
  handleTryToCompleteTask,
  handleUpdateTask,
  handleDeleteTask
} from '../../handlers/task.jsx';
import styles from './TaskDetails.module.css';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const TaskDetails = () => {
  const { task_id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();

  const fetchTaskData = async () => {
    try {
      await handleGetTask(task_id, setTask, setLoading, setUserRole);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchTaskData();
  }, [task_id]);

  const handleSubmitAnswer = async () => {
    try {
      setIsSubmitting(true);
      const values = await form.validateFields();
      await handleTryToCompleteTask(task_id, values.answer, fetchTaskData);
    } catch (err) {
      message.error(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateTask = async () => {
    try {
      setIsSubmitting(true);
      const values = await editForm.validateFields();
      await handleUpdateTask(task_id, values, setTask);
      setIsEditModalVisible(false);
    } catch (err) {
      message.error(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteTask = async () => {
    try {
      await handleDeleteTask(task_id, task.module_id, navigate);
    } catch (err) {
      message.error(err.message);
    }
  };

  const formatDate = (dateString) => {
    return dayjs(dateString).format('DD.MM.YYYY HH:mm');
  };

  const isAdminOrTeacher = userRole === 0 || userRole === 1;
  const isTaskCompleted = task?.is_correct;
  const attemptsExhausted = task?.user_attempts >= task?.max_attempts;

  if (loading) return (
    <div className={styles.loadingContainer}>
      <Spin size="large" />
    </div>
  );

  if (error) return <Alert type="error" message={error} className={styles.errorAlert} />;
  if (!task) return <Alert type="warning" message="Задание не найдено" className={styles.warningAlert} />;

  return (
    <div className={styles.container}>
      <Button
        type="text"
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate(-1)}
        className={styles.backButton}
      >
        Назад
      </Button>

      <Card
        title={
          <div className={styles.header}>
            <Title level={2} className={styles.title}>{task.title}</Title>
            {isAdminOrTeacher && (
              <Space className={styles.actions}>
                <Button
                  type="default"
                  icon={<EditOutlined />}
                  onClick={() => {
                    setIsEditModalVisible(true);
                    editForm.setFieldsValue({
                      title: task.title,
                      description: task.description,
                      correct_answer: task.correct_answer,
                      max_attempts: task.max_attempts,
                      dateRange: [
                        dayjs(task.start_datetime),
                        dayjs(task.end_datetime)
                      ]
                    });
                  }}
                  className={styles.editButton}
                >
                  Редактировать
                </Button>
                <Popconfirm
                  title="Вы уверены, что хотите удалить это задание?"
                  description="Это действие нельзя отменить. Все ответы пользователей на это задание также будут удалены."
                  onConfirm={handleDeleteTask}
                  okText="Да, удалить"
                  cancelText="Отмена"
                  okButtonProps={{ danger: true }}
                >
                  <Button danger icon={<DeleteOutlined />} className={styles.deleteButton}>
                    Удалить
                  </Button>
                </Popconfirm>
              </Space>
            )}
          </div>
        }
        className={styles.card}
      >
        <Row gutter={16} className={styles.statsRow}>
          <Col xs={24} sm={12} md={8}>
            <Statistic
              title="Статус"
              value={isTaskCompleted ? 'Правильно' : attemptsExhausted ? 'Неверно' : 'Не проверено'}
              prefix={isTaskCompleted ?
                <CheckOutlined className={styles.successIcon} /> :
                attemptsExhausted ?
                <CloseOutlined className={styles.errorIcon} /> :
                <ClockCircleOutlined className={styles.warningIcon} />}
              className={styles.statistic}
            />
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Statistic
              title="Попытки"
              value={`${task.user_attempts} / ${task.max_attempts}`}
              className={styles.statistic}
            />
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Statistic
              title="Срок сдачи"
              value={formatDate(task.end_datetime)}
              className={styles.statistic}
            />
          </Col>
        </Row>

        <Divider className={styles.divider} />

        <Title level={4} className={styles.sectionTitle}>Описание задания:</Title>
        <Paragraph className={styles.description}>{task.description}</Paragraph>

        <Divider className={styles.divider} />

        <Title level={4} className={styles.sectionTitle}>Ваш ответ:</Title>
        <Form form={form} layout="vertical" className={styles.form}>
          <Form.Item
            name="answer"
            rules={[{ required: true, message: 'Пожалуйста, введите ваш ответ' }]}
            className={styles.formItem}
          >
            <TextArea
              rows={6}
              placeholder="Введите ваш ответ здесь..."
              disabled={attemptsExhausted || isTaskCompleted}
              className={styles.textarea}
            />
          </Form.Item>

          {isTaskCompleted && (
            <Alert
              message="Вы успешно выполнили это задание!"
              type="success"
              showIcon
              className={styles.alert}
            />
          )}

          {attemptsExhausted && !isTaskCompleted && (
            <Alert
              message="Вы исчерпали все попытки для этого задания"
              type="warning"
              showIcon
              className={styles.alert}
            />
          )}

          {!attemptsExhausted && !isTaskCompleted && (
            <Space className={styles.submitSection}>
              <Button
                type="primary"
                onClick={handleSubmitAnswer}
                loading={isSubmitting}
                disabled={loading}
                className={styles.submitButton}
              >
                Отправить ответ
              </Button>
              <Text type="secondary" className={styles.attemptsText}>
                Осталось попыток: {task.max_attempts - task.user_attempts}
              </Text>
            </Space>
          )}
        </Form>
      </Card>

      <Modal
        title="Редактирование задания"
        open={isEditModalVisible}
        onCancel={() => setIsEditModalVisible(false)}
        onOk={handleUpdateTask}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={isSubmitting}
        className={styles.modal}
      >
        <Form form={editForm} layout="vertical" className={styles.editForm}>
          <Form.Item
            name="title"
            label="Название"
            rules={[{ required: true, message: 'Введите название задания' }]}
            className={styles.formItem}
          >
            <Input className={styles.input} />
          </Form.Item>
          <Form.Item
            name="description"
            label="Описание"
            rules={[{ required: true, message: 'Введите описание задания' }]}
            className={styles.formItem}
          >
            <TextArea rows={4} className={styles.textarea} />
          </Form.Item>
          <Form.Item
            name="correct_answer"
            label="Правильный ответ"
            rules={[{ required: true, message: 'Введите правильный ответ' }]}
            className={styles.formItem}
          >
            <Input className={styles.input} />
          </Form.Item>
          <Form.Item
            name="max_attempts"
            label="Макс. попыток"
            rules={[{ required: true, message: 'Введите количество попыток' }]}
            className={styles.formItem}
          >
            <InputNumber min={1} max={10} className={styles.inputNumber} />
          </Form.Item>
          <Form.Item
            name="dateRange"
            label="Период времени"
            rules={[{ required: true, message: 'Выберите период времени' }]}
            className={styles.formItem}
          >
            <DatePicker.RangePicker
              showTime
              className={styles.datePicker}
              disabledDate={(current) => current && current < dayjs().startOf('day')}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TaskDetails;