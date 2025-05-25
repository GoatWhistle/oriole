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
  Col
} from 'antd';
import {
  CheckOutlined,
  CloseOutlined,
  EditOutlined,
  ClockCircleOutlined,
  ArrowLeftOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const TaskDetails = () => {
    const { task_id } = useParams();
    const navigate = useNavigate();
    const [task, setTask] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [form] = Form.useForm();

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

                // Устанавливаем текущий ответ пользователя в форму
                form.setFieldsValue({
                    answer: taskData.user_answer || ''
                });
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

            const response = await fetch(`/api/v1/tasks/${task_id}/submit/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    user_answer: values.answer
                })
            });

            if (!response.ok) {
                throw new Error('Не удалось отправить ответ');
            }

            const result = await response.json();
            message.success('Ответ успешно отправлен');

            // Обновляем данные задания после отправки ответа
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

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

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

            <Card>
                <Title level={2}>{task.title}</Title>

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
        </div>
    );
};

export default TaskDetails;