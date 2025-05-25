import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Divider,
  Button,
  Space,
  Tag,
  message,
  Form,
  Input,
  Alert,
  Statistic,
  Row,
  Col,
  Modal,
  Popconfirm,
  DatePicker
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
    const [showResult, setShowResult] = useState(false);
    const [resultCorrect, setResultCorrect] = useState(null);
    const [form] = Form.useForm();
    const [editForm] = Form.useForm();

    useEffect(() => {
        const fetchTask = async () => {
            try {
                setLoading(true);
                const response = await fetch(`/api/v1/tasks/${task_id}/`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                if (!response.ok) {
                    throw new Error('Не удалось загрузить информацию о задании');
                }

                const taskData = await response.json();
                setTask(taskData);

                form.setFieldsValue({
                    answer: taskData.user_answer || ''
                });

                const assignmentResponse = await fetch(`/api/v1/assignments/${taskData.assignment_id}/`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                if (assignmentResponse.ok) {
                    const assignmentData = await assignmentResponse.json();
                    const roleResponse = await fetch(`/api/v1/auth/get-role/group/${assignmentData.group_id}`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    });

                    if (roleResponse.ok) {
                        const role = await roleResponse.json();
                        setUserRole(role);
                    }
                }
            } catch (err) {
                setError(err.message);
                message.error(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTask();
    }, [task_id, form]);

    const handleSubmitAnswer = async () => {
        try {
            setIsSubmitting(true);
            const values = await form.validateFields();
            const userAnswer = values.answer;

            const response = await fetch(`/api/v1/tasks/${task_id}/complete/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    user_answer: userAnswer
                })
            });

            if (!response.ok) {
                throw new Error('Не удалось отправить ответ на проверку');
            }

            const result = await response.json();

            // Показываем результат проверки
            setResultCorrect(result.is_correct);
            setShowResult(true);

            if (result.is_correct) {
                message.success('Правильный ответ!');
            } else {
                message.error('Неправильный ответ! Попробуйте еще раз.');
            }

            // Обновляем данные задания
            const updatedResponse = await fetch(`/api/v1/tasks/${task_id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            if (updatedResponse.ok) {
                const updatedTask = await updatedResponse.json();
                setTask(updatedTask);
            }
        } catch (err) {
            message.error(err.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdateTask = async () => {
        try {
            const values = await editForm.validateFields();
            const response = await fetch(`/api/v1/tasks/${task_id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    ...values,
                    start_datetime: values.dateRange[0].toISOString(),
                    end_datetime: values.dateRange[1].toISOString()
                })
            });

            if (!response.ok) {
                throw new Error('Не удалось обновить задание');
            }

            const updatedTask = await response.json();
            setTask(updatedTask);
            message.success('Задание успешно обновлено');
            setIsEditModalVisible(false);
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDeleteTask = async () => {
        try {
            const response = await fetch(`/api/v1/tasks/${task_id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Не удалось удалить задание');
            }

            message.success('Задание успешно удалено');
            navigate(`/assignments/${task.assignment_id}`);
        } catch (err) {
            message.error(err.message);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    const isAdmin = userRole === 0 || userRole === 1;

    if (loading) return <div>Загрузка информации о задании...</div>;
    if (error) return <div>Ошибка: {error}</div>;
    if (!task) return <div>Задание не найдено</div>;

    return (
        <div style={{ padding: '24px' }}>
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
                        {isAdmin && (
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
                                    onConfirm={handleDeleteTask}
                                    okText="Да"
                                    cancelText="Нет"
                                >
                                    <Button danger icon={<DeleteOutlined />}>
                                        Удалить
                                    </Button>
                                </Popconfirm>
                            </Space>
                        )}
                    </div>
                }
            >
                <Row gutter={16} style={{ marginBottom: 24 }}>
                    <Col span={8}>
                        <Statistic
                            title="Статус"
                            value={task.is_correct ? 'Правильно' : 'Не проверено'}
                            prefix={task.is_correct ? <CheckOutlined style={{ color: '#52c41a' }} /> : <ClockCircleOutlined />}
                        />
                    </Col>
                    <Col span={8}>
                        <Statistic
                            title="Попытки"
                            value={`${task.user_attempts} / ${task.max_attempts}`}
                        />
                    </Col>
                    <Col span={8}>
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
                            disabled={task.user_attempts >= task.max_attempts}
                        />
                    </Form.Item>

                    {showResult && (
                        <Alert
                            message={resultCorrect ? 'Правильный ответ!' : 'Неправильный ответ!'}
                            type={resultCorrect ? 'success' : 'error'}
                            showIcon
                            style={{ marginBottom: 16 }}
                        />
                    )}

                    {task.user_attempts >= task.max_attempts ? (
                        <Alert
                            message="Вы исчерпали все попытки для этого задания"
                            type="warning"
                            showIcon
                        />
                    ) : (
                        <Space>
                            <Button
                                type="primary"
                                onClick={handleSubmitAnswer}
                                loading={isSubmitting}
                            >
                                Отправить ответ
                            </Button>
                            <Text type="secondary">
                                Осталось попыток: {task.max_attempts - task.user_attempts}
                            </Text>
                        </Space>
                    )}
                </Form>

                {task.user_answer && (
                    <>
                        <Divider />
                        <Title level={4}>Предыдущие ответы:</Title>
                        <Card>
                            <Paragraph strong>Ваш ответ:</Paragraph>
                            <Paragraph style={{ whiteSpace: 'pre-line' }}>{task.user_answer}</Paragraph>
                            {task.is_correct !== null && (
                                <Paragraph>
                                    <Tag
                                        color={task.is_correct ? 'success' : 'error'}
                                        icon={task.is_correct ? <CheckOutlined /> : <CloseOutlined />}
                                    >
                                        {task.is_correct ? 'Правильно' : 'Неправильно'}
                                    </Tag>
                                </Paragraph>
                            )}
                        </Card>
                    </>
                )}
            </Card>

            <Modal
                title="Редактирование задания"
                visible={isEditModalVisible}
                onCancel={() => setIsEditModalVisible(false)}
                onOk={handleUpdateTask}
                okText="Сохранить"
                cancelText="Отмена"
                width={800}
            >
                <Form
                    form={editForm}
                    layout="vertical"
                >
                    <Form.Item
                        name="title"
                        label="Название задания"
                        rules={[{ required: true, message: 'Введите название задания' }]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="description"
                        label="Описание задания"
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
                        label="Максимальное количество попыток"
                        rules={[{ required: true, message: 'Укажите количество попыток' }]}
                    >
                        <InputNumber min={1} style={{ width: '100%' }} />
                    </Form.Item>

                    <Form.Item
                        name="dateRange"
                        label="Срок выполнения"
                        rules={[{ required: true, message: 'Укажите срок выполнения' }]}
                    >
                        <DatePicker.RangePicker
                            showTime
                            style={{ width: '100%' }}
                            disabledDate={(current) => {
                                return current && current < dayjs().startOf('day');
                            }}
                        />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default TaskDetails;