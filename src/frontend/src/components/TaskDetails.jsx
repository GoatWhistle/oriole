import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Divider,
  Button,
  Space,
  message,
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
import axios from 'axios';

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
            setLoading(true);
            const taskResponse = await fetch(`/api/v1/tasks/${task_id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            if (!taskResponse.ok) {
                throw new Error('Не удалось загрузить информацию о задании');
            }

            const taskData = await taskResponse.json();
            setTask(taskData);
            form.setFieldsValue({ answer: taskData.user_answer || '' });

            if (taskData.assignment_id) {
                try {
                    const assignmentResponse = await fetch(`/api/v1/assignments/${taskData.assignment_id}/`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    });

                    if (assignmentResponse.ok) {
                        const assignmentData = await assignmentResponse.json();
                        const roleResponse = await fetch(`/api/v1/users/get-role/group/${assignmentData.group_id}`, {
                            headers: {
                                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                            }
                        });

                        if (roleResponse.ok) {
                            setUserRole(await roleResponse.json());
                        }
                    }
                } catch (err) {
                    console.error("Ошибка при загрузке роли пользователя:", err);
                }
            }
        } catch (err) {
            setError(err.message);
            message.error(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTaskData();
    }, [task_id]);

    const handleSubmitAnswer = async () => {
        try {
            setIsSubmitting(true);
            const values = await form.validateFields();
            const user_answer = values.answer;

            const response = await axios.patch(
                `/api/v1/tasks/${task_id}/complete/?user_answer=${encodeURIComponent(user_answer)}`,
                {},
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                        'Accept': 'application/json'
                    },
                    withCredentials: true
                }
            );

            await fetchTaskData();
            message.success(response.data.is_correct ?
                'Правильный ответ!' :
                'Неправильный ответ! Попробуйте еще раз.');

        } catch (err) {
            await fetchTaskData();
            message.error(err.response?.data?.detail || 'Ошибка при отправке ответа');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdateTask = async () => {
        try {
            const values = await editForm.validateFields();
            const response = await axios.patch(
                `/api/v1/tasks/${task_id}/`,
                {
                    ...values,
                    start_datetime: values.dateRange[0].toISOString(),
                    end_datetime: values.dateRange[1].toISOString()
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                }
            );

            setTask(response.data);
            message.success('Задание успешно обновлено');
            setIsEditModalVisible(false);
        } catch (err) {
            message.error(err.response?.data?.detail || err.message);
        }
    };

    const handleDeleteTask = async () => {
        try {
            await axios.delete(`/api/v1/tasks/${task_id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            message.success('Задание успешно удалено');
            navigate(`/assignments/${task.assignment_id}`);
        } catch (err) {
            message.error(err.response?.data?.detail || 'Не удалось удалить задание');
        }
    };

    const formatDate = (dateString) => {
        return dayjs(dateString).format('DD.MM.YYYY HH:mm');
    };

    const isAdminOrTeacher = userRole === 0 || userRole === 1;
    const isTaskCompleted = task?.is_correct;
    const attemptsExhausted = task?.user_attempts >= task?.max_attempts;

    if (loading) return (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '24px' }}>
            <Spin size="large" />
        </div>
    );

    if (error) return <Alert type="error" message={error} />;
    if (!task) return <Alert type="warning" message="Задание не найдено" />;

    return (
        <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
            <Button
                type="text"
                icon={<ArrowLeftOutlined />}
                onClick={() => navigate(-1)}
                style={{ marginBottom: 16 }}
            >
                Назад
            </Button>

            <Card
                title={
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Title level={2} style={{ margin: 0 }}>{task.title}</Title>
                        {isAdminOrTeacher && (
                            <Space>
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
                                    <Button danger icon={<DeleteOutlined />}>
                                        Удалить
                                    </Button>
                                </Popconfirm>
                            </Space>
                        )}
                    </div>
                }
                loading={loading}
            >
                <Row gutter={16} style={{ marginBottom: 24 }}>
                    <Col xs={24} sm={12} md={8}>
                        <Statistic
                            title="Статус"
                            value={isTaskCompleted ? 'Правильно' : attemptsExhausted ? 'Неверно' : 'Не проверено'}
                            prefix={isTaskCompleted ?
                                <CheckOutlined style={{ color: '#52c41a' }} /> :
                                attemptsExhausted ?
                                <CloseOutlined style={{ color: '#ff4d4f' }} /> :
                                <ClockCircleOutlined />}
                        />
                    </Col>
                    <Col xs={24} sm={12} md={8}>
                        <Statistic
                            title="Попытки"
                            value={`${task.user_attempts} / ${task.max_attempts}`}
                        />
                    </Col>
                    <Col xs={24} sm={12} md={8}>
                        <Statistic
                            title="Срок сдачи"
                            value={formatDate(task.end_datetime)}
                        />
                    </Col>
                </Row>

                <Divider />

                <Title level={4}>Описание задания:</Title>
                <Paragraph style={{ whiteSpace: 'pre-line' }}>{task.description}</Paragraph>

                <Divider />

                <Title level={4}>Ваш ответ:</Title>
                <Form form={form} layout="vertical">
                    <Form.Item
                        name="answer"
                        rules={[{ required: true, message: 'Пожалуйста, введите ваш ответ' }]}
                    >
                        <TextArea
                            rows={6}
                            placeholder="Введите ваш ответ здесь..."
                            disabled={attemptsExhausted || isTaskCompleted}
                        />
                    </Form.Item>

                    {isTaskCompleted && (
                        <Alert
                            message="Вы успешно выполнили это задание!"
                            type="success"
                            showIcon
                            style={{ marginBottom: 16 }}
                        />
                    )}

                    {attemptsExhausted && !isTaskCompleted && (
                        <Alert
                            message="Вы исчерпали все попытки для этого задания"
                            type="warning"
                            showIcon
                            style={{ marginBottom: 16 }}
                        />
                    )}

                    {!attemptsExhausted && !isTaskCompleted && (
                        <Space>
                            <Button
                                type="primary"
                                onClick={handleSubmitAnswer}
                                loading={isSubmitting}
                                disabled={loading}
                            >
                                Отправить ответ
                            </Button>
                            <Text type="secondary">
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
            >
                <Form form={editForm} layout="vertical">
                    <Form.Item
                        name="title"
                        label="Название"
                        rules={[{ required: true, message: 'Введите название задания' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="description"
                        label="Описание"
                        rules={[{ required: true, message: 'Введите описание задания' }]}
                    >
                        <TextArea rows={4} />
                    </Form.Item>
                    <Form.Item
                        name="correct_answer"
                        label="Правильный ответ"
                        rules={[{ required: true, message: 'Введите правильный ответ' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="max_attempts"
                        label="Макс. попыток"
                        rules={[{ required: true, message: 'Введите количество попыток' }]}
                    >
                        <InputNumber min={1} max={10} style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item
                        name="dateRange"
                        label="Период времени"
                        rules={[{ required: true, message: 'Выберите период времени' }]}
                    >
                        <DatePicker.RangePicker
                            showTime
                            style={{ width: '100%' }}
                            disabledDate={(current) => current && current < dayjs().startOf('day')}
                        />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default TaskDetails;
