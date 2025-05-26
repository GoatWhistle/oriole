import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Divider,
  Progress,
  List,
  message,
  Tag,
  Button,
  Modal,
  Form,
  Input,
  InputNumber,
  DatePicker,
  Space,
  Popconfirm
} from 'antd';
import dayjs from 'dayjs';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const AssignmentDetails = () => {
    const { assignment_id } = useParams();
    const navigate = useNavigate();
    const [assignment, setAssignment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userData, setUserData] = useState(null);
    const [userRole, setUserRole] = useState(null);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isEditModalVisible, setIsEditModalVisible] = useState(false);
    const [form] = Form.useForm();
    const [editForm] = Form.useForm();

    useEffect(() => {
        const checkAuthentication = async () => {
            try {
                setLoading(true);
                // Загружаем данные задания
                const assignmentResponse = await fetch(`/api/v1/assignments/${assignment_id}/`);

                if (!assignmentResponse.ok) {
                    throw new Error('Не удалось загрузить информацию о задании');
                }

                const assignmentData = await assignmentResponse.json();
                setAssignment(assignmentData);

                // Получаем роль пользователя в группе
                const roleResponse = await fetch(`/api/v1/auth/get-role/group/${assignmentData.group_id}`);

                if (!roleResponse.ok) {
                    throw new Error('Не удалось получить информацию о роли пользователя');
                }

                const role = await roleResponse.json();
                setUserRole(role);

                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
                message.error(err.message);
            }
        };

        checkAuthentication(); // Вызываем функцию
    }, [assignment_id]); // Добавляем зависимость assignment_id

    const handleCreateTask = async (values) => {
        try {
            const response = await fetch('/api/v1/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...values,
                    assignment_id: parseInt(assignment_id),
                    start_datetime: values.dateRange[0].toISOString(),
                    end_datetime: values.dateRange[1].toISOString()
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка при создании задания');
            }

            const task = await response.json();
            message.success('Задание успешно создано!');
            setIsModalVisible(false);
            form.resetFields();

            // Обновляем список заданий
            const updatedResponse = await fetch(`/api/v1/assignments/${assignment_id}/`);
            const updatedData = await updatedResponse.json();
            setAssignment(updatedData);

            // Переходим к созданному заданию
            navigate(`/tasks/${task.id}`);
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDeleteAssignment = async () => {
        try {
            const response = await fetch(`/api/v1/assignments/${assignment_id}/`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Ошибка при удалении модуля');
            }

            message.success('Модуль успешно удален!');
            navigate('/assignments');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleUpdateAssignment = async (values) => {
        try {
            const response = await fetch(`/api/v1/assignments/${assignment_id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...values,
                    start_datetime: values.dateRange?.[0]?.toISOString(),
                    end_datetime: values.dateRange?.[1]?.toISOString()
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка при обновлении модуля');
            }

            const updatedAssignment = await response.json();
            setAssignment(updatedAssignment);
            message.success('Модуль успешно обновлен!');
            setLoading(false);
            setIsEditModalVisible(false);
            editForm.resetFields();
        } catch (err) {
            message.error(err.message);
        }
    };

    if (loading) return <div>Загрузка задания...</div>;
    if (error) return <div>Ошибка: {error}</div>;
    if (!assignment) return <div>Задание не найдено</div>;

    const completionPercentage = assignment.tasks_count > 0
        ? Math.round((assignment.user_completed_tasks_count / assignment.tasks_count) * 100)
        : 0;

    const startDate = dayjs(assignment.start_datetime).format('DD.MM.YYYY HH:mm');
    const endDate = dayjs(assignment.end_datetime).format('DD.MM.YYYY HH:mm');

    // Проверяем, имеет ли пользователь права администратора (роль 0 или 1)
    const isAdmin = userRole === 0 || userRole === 1;

    return (
        <div style={{ padding: '24px' }}>
            {userData && (
                <div style={{ marginBottom: '16px', textAlign: 'right' }}>
                    <Text strong>
                        {userData.profile.surname} {userData.profile.name}
                    </Text>
                </div>
            )}

            <Card
                title={
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Title level={2} style={{ margin: 0 }}>{assignment.title}</Title>
                        <Space>
                            <Button
                                type="primary"
                                onClick={() => setIsModalVisible(true)}
                            >
                                Создать задание
                            </Button>
                            {isAdmin && (
                                <>
                                    <Button
                                        type="default"
                                        onClick={() => {
                                            setIsEditModalVisible(true);
                                            editForm.setFieldsValue({
                                                title: assignment.title,
                                                description: assignment.description,
                                                is_contest: assignment.is_contest,
                                                dateRange: [
                                                    dayjs(assignment.start_datetime),
                                                    dayjs(assignment.end_datetime)
                                                ]
                                            });
                                        }}
                                    >
                                        Редактировать модуль
                                    </Button>
                                    <Popconfirm
                                        title="Вы уверены, что хотите удалить этот модуль?"
                                        onConfirm={handleDeleteAssignment}
                                        okText="Да"
                                        cancelText="Нет"
                                    >
                                        <Button danger>
                                            Удалить модуль
                                        </Button>
                                    </Popconfirm>
                                </>
                            )}
                        </Space>
                    </div>
                }
            >
                <Paragraph>{assignment.description}</Paragraph>

                <div style={{ margin: '16px 0' }}>
                    <Tag color={assignment.is_active ? 'green' : 'red'}>
                        {assignment.is_active ? 'Активно' : 'Неактивно'}
                    </Tag>
                    <Tag color={assignment.is_contest ? 'orange' : 'blue'}>
                        {assignment.is_contest ? 'Конкурс' : 'Обычное задание'}
                    </Tag>
                </div>

                <Divider />

                <Text strong>Сроки выполнения:</Text>
                <Paragraph>
                    Начало: {startDate}<br />
                    Окончание: {endDate}
                </Paragraph>

                <Divider />

                <Text strong>Прогресс выполнения:</Text>
                <Progress
                    percent={completionPercentage}
                    status={completionPercentage === 100 ? 'success' : 'active'}
                />
                <Text>
                    {assignment.user_completed_tasks_count} из {assignment.tasks_count} заданий выполнено
                </Text>

                <Divider />

                <Title level={4}>Задачи:</Title>
                <List
                    dataSource={assignment.tasks}
                    renderItem={task => (
                        <List.Item>
                            <Card
                                size="small"
                                title={task.title}
                                style={{ width: '100%' }}
                                extra={
                                    <div>
                                        {task.is_correct !== undefined && (
                                            task.is_correct ?
                                                <Tag color="success">Выполнено</Tag> :
                                                <Tag color="warning">Не выполнено</Tag>
                                        )}
                                        <Tag color={task.is_active ? 'green' : 'red'}>
                                            {task.is_active ? 'Активна' : 'Неактивна'}
                                        </Tag>
                                    </div>
                                }
                            >
                                <Paragraph>{task.description}</Paragraph>
                                <Button
                                    type="primary"
                                    onClick={() => navigate(`/tasks/${task.id}`)}
                                >
                                    Перейти к задаче
                                </Button>
                            </Card>
                        </List.Item>
                    )}
                />
            </Card>

            {/* Модальное окно создания задачи */}
            <Modal
                title="Создание нового задания"
                visible={isModalVisible}
                onCancel={() => {
                    setIsModalVisible(false);
                    form.resetFields();
                }}
                onOk={() => form.submit()}
                okText="Создать"
                cancelText="Отмена"
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleCreateTask}
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
                                // Запрещаем выбирать даты раньше текущей
                                return current && current < dayjs().startOf('day');
                            }}
                        />
                    </Form.Item>
                </Form>
            </Modal>

            {/* Модальное окно редактирования модуля (только для админов) */}
            {isAdmin && (
                <Modal
                    title="Редактирование модуля"
                    visible={isEditModalVisible}
                    onCancel={() => {
                        setIsEditModalVisible(false);
                        editForm.resetFields();
                    }}
                    onOk={() => editForm.submit()}
                    okText="Сохранить"
                    cancelText="Отмена"
                >
                    <Form
                        form={editForm}
                        layout="vertical"
                        onFinish={handleUpdateAssignment}
                    >
                        <Form.Item
                            name="title"
                            label="Название модуля"
                            rules={[{ required: true, message: 'Введите название модуля' }]}
                        >
                            <Input />
                        </Form.Item>

                        <Form.Item
                            name="description"
                            label="Описание модуля"
                            rules={[{ required: true, message: 'Введите описание модуля' }]}
                        >
                            <TextArea rows={4} />
                        </Form.Item>

                        <Form.Item
                            name="is_contest"
                            label="Тип модуля"
                            valuePropName="checked"
                        >
                            <Input type="checkbox" /> Конкурс
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
            )}
        </div>
    );
};

export default AssignmentDetails;