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
  Popconfirm,
  Checkbox
} from 'antd';
import dayjs from 'dayjs';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const ModuleDetails = () => {
    const { module_id } = useParams();
    const navigate = useNavigate();
    const [module, setModule] = useState(null);
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
                const moduleResponse = await fetch(`/api/modules/${module_id}/`);

                if (!moduleResponse.ok) {
                    throw new Error('Не удалось загрузить информацию о задании');
                }

                const moduleData = await moduleResponse.json();
                setModule(moduleData);
                console.log(moduleData);

                const roleResponse = await fetch(`/api/users/get-role/group/${moduleData.group_id}`);

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

        checkAuthentication();
    }, [module_id]);

    const handleCreateTask = async (values) => {
        try {
            const response = await fetch('/api/tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...values,
                    module_id: parseInt(module_id),
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

            const updatedResponse = await fetch(`/api/modules/${module_id}/`);
            const updatedData = await updatedResponse.json();
            setModule(updatedData);

            navigate(`/tasks/${task.id}`);
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDeleteModule = async () => {
        try {
            const response = await fetch(`/api/modules/${module_id}/`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Ошибка при удалении модуля');
            }

            message.success('Модуль успешно удален!');
            navigate('/');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleUpdateModule = async (values) => {
        try {
            const response = await fetch(`/api/modules/${module_id}/`, {
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

            const updatedModule = await response.json();
            setModule(updatedModule);
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
    if (!module) return <div>Задание не найдено</div>;

    const completionPercentage = module.tasks_count > 0
        ? Math.round((module.user_completed_tasks_count / module.tasks_count) * 100)
        : 0;

    const startDate = dayjs(module.start_datetime).format('DD.MM.YYYY HH:mm');
    const endDate = dayjs(module.end_datetime).format('DD.MM.YYYY HH:mm');

    const isAdmin = userRole === 0 || userRole === 1;

    const disabledDateForTask = (current) => {
        const moduleStart = dayjs(module.start_datetime);
        const moduleEnd = dayjs(module.end_datetime);
        return current && (
            current < moduleStart.startOf('day') ||
            current > moduleEnd.endOf('day')
        );
    };

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
                        <Title level={2} style={{ margin: 0 }}>{module.title}</Title>
                        <Space>
                            {isAdmin && (
                                <>
                                    <Button
                                        type="primary"
                                        onClick={() => setIsModalVisible(true)}
                                    >
                                        Создать задание
                                    </Button>
                                    <Button
                                        type="default"
                                        onClick={() => {
                                            setIsEditModalVisible(true);
                                            editForm.setFieldsValue({
                                                title: module.title,
                                                description: module.description,
                                                is_contest: module.is_contest,
                                                dateRange: [
                                                    dayjs(module.start_datetime),
                                                    dayjs(module.end_datetime)
                                                ]
                                            });
                                        }}
                                    >
                                        Редактировать модуль
                                    </Button>
                                    <Popconfirm
                                        title="Вы уверены, что хотите удалить этот модуль?"
                                        onConfirm={handleDeleteModule}
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
                <Paragraph>{module.description}</Paragraph>

                <div style={{ margin: '16px 0' }}>
                    <Tag color={module.is_active ? 'green' : 'red'}>
                        {module.is_active ? 'Активно' : 'Неактивно'}
                    </Tag>
                    <Tag color={module.is_contest ? 'orange' : 'transparent'}>
                        {module.is_contest ? 'Контест' : ''}
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
                    {module.user_completed_tasks_count} из {module.tasks_count} заданий выполнено
                </Text>

                <Divider />

                <Title level={4}>Задачи:</Title>
                <List
                    dataSource={module.tasks}
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
                            disabledDate={disabledDateForTask}
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
                        onFinish={handleUpdateModule}
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
                            <Checkbox>Контест</Checkbox>
                        </Form.Item>

                        <Form.Item
                            name="dateRange"
                            label="Срок выполнения"
                            rules={[{ required: true, message: 'Укажите срок выполнения' }]}
                        >
                            <DatePicker.RangePicker
                                showTime
                                style={{ width: '100%' }}
                            />
                        </Form.Item>
                    </Form>
                </Modal>
            )}
        </div>
    );
};

export default ModuleDetails;