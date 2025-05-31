import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Card,
  Typography,
  Divider,
  List,
  Avatar,
  Tag,
  message,
  Button,
  Modal,
  Input,
  Popconfirm,
  Form,
  Space,
  DatePicker,
  Switch,
  Row,
  Col,
  InputNumber,
  Select,
  Alert
} from 'antd';
import {
  CopyOutlined,
  CloseOutlined,
  EditOutlined,
  LogoutOutlined,
  PlusOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  ClockCircleOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { RangePicker } = DatePicker;
const { Option } = Select;

const GroupDetails = () => {
    const { group_id } = useParams();
    const navigate = useNavigate();
    const [group, setGroup] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userRole, setUserRole] = useState(null);
    const [inviteLink, setInviteLink] = useState(null);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isEditModalVisible, setIsEditModalVisible] = useState(false);
    const [isCreateAssignmentModalVisible, setIsCreateAssignmentModalVisible] = useState(false);
    const [isInviteSettingsModalVisible, setIsInviteSettingsModalVisible] = useState(false);
    const [expiryTime, setExpiryTime] = useState(null);
    const [expiresMinutes, setExpiresMinutes] = useState(30);
    const [inviteType, setInviteType] = useState('single_use');
    const [form] = Form.useForm();
    const [assignmentForm] = Form.useForm();

    useEffect(() => {
        const detectTimezone = () => {
            try {
                return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
            } catch (e) {
                return 'UTC';
            }
        };

        const fetchData = async () => {
            try {
                setLoading(true);

                const [groupResponse, roleResponse] = await Promise.all([
                    fetch(`/api/v1/groups/${group_id}/`),
                    fetch(`/api/v1/users/get-role/group/${group_id}/`)
                ]);

                if (!groupResponse.ok) {
                    throw new Error('Не удалось загрузить информацию о группе');
                }
                const groupData = await groupResponse.json();

                if (!roleResponse.ok) {
                    throw new Error('Не удалось определить вашу роль в группе');
                }
                const roleData = await roleResponse.json();

                setGroup(groupData);
                setUserRole(roleData);
            } catch (err) {
                setError(err.message);
                message.error(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [group_id]);

    const handleGenerateInviteLink = async () => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/invite/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    expires_minutes: expiresMinutes,
                    single_use: inviteType === 'single_use'
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Не удалось сгенерировать ссылку для вступления');
            }

            const data = await response.json();
            setInviteLink(data.link);

            const expiry = new Date();
            expiry.setMinutes(expiry.getMinutes() + expiresMinutes);
            setExpiryTime(expiry);

            setIsModalVisible(true);
            setIsInviteSettingsModalVisible(false);
            message.success('Ссылка для вступления успешно создана');
        } catch (err) {
            console.error("Ошибка при генерации ссылки:", err);
            message.error(err.message || 'Ошибка при генерации ссылки');
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(inviteLink);
        message.success('Ссылка скопирована в буфер обмена');
    };

    const getRoleName = (role) => {
        const roles = {
            0: 'Создатель',
            1: 'Учитель',
            2: 'Ученик'
        };
        return roles[role] || 'Неизвестная роль';
    };

    const handleAssignmentClick = (assignmentId) => {
        navigate(`/assignments/${assignmentId}`);
    };

    const handleRemoveUser = async (userId) => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/kick/${userId}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Не удалось удалить пользователя из группы');
            }

            setGroup(prev => ({
                ...prev,
                accounts: prev.accounts.filter(account => account.user_id !== userId)
            }));

            message.success('Пользователь успешно удален из группы');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleLeaveGroup = async () => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/leave/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Не удалось выйти из группы');
            }

            message.success('Вы успешно вышли из группы');
            navigate('/');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handlePromoteToTeacher = async (userId) => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/promote/${userId}/`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                throw new Error('Не удалось повысить пользователя до учителя');
            }

            setGroup(prev => ({
                ...prev,
                accounts: prev.accounts.map(account =>
                    account.user_id === userId ? { ...account, role: 1 } : account
                )
            }));

            message.success('Пользователь повышен до учителя');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDemoteToStudent = async (userId) => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/demote/${userId}/`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                throw new Error('Не удалось понизить пользователя до ученика');
            }

            setGroup(prev => ({
                ...prev,
                accounts: prev.accounts.map(account =>
                    account.user_id === userId ? { ...account, role: 2 } : account
                )
            }));

            message.success('Пользователь понижен до ученика');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDeleteGroup = async () => {
        try {
            const response = await fetch(`/api/v1/groups/${group_id}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Не удалось удалить группу');
            }

            message.success('Группа успешно удалена');
            navigate('/');
        } catch (err) {
            message.error(err.message);
        }
    };

    const showEditModal = () => {
        form.setFieldsValue({
            title: group.title,
            description: group.description
        });
        setIsEditModalVisible(true);
    };

    const handleEditSubmit = async () => {
        try {
            const values = await form.validateFields();
            const response = await fetch(`/api/v1/groups/${group_id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values)
            });

            if (!response.ok) {
                throw new Error('Не удалось обновить информацию о группе');
            }

            const updatedGroup = await response.json();
            setGroup(updatedGroup);
            setIsEditModalVisible(false);
            message.success('Информация о группе успешно обновлена');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleCreateAssignment = async () => {
        try {
            const values = await assignmentForm.validateFields();

            // Format data exactly as the working curl example
            const assignmentData = {
                title: values.title,
                description: values.description || "string", // Fallback to "string" if empty
                is_contest: values.is_contest || false,
                group_id: parseInt(group_id),
                start_datetime: values.dateRange[0].toISOString(),
                end_datetime: values.dateRange[1].toISOString()
            };

            console.log("Submitting assignment:", assignmentData);

            const response = await axios.post('/api/v1/assignments/',
                assignmentData,
                {
                    headers: {
                        'accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    withCredentials: true
                }
            );

            console.log("Assignment created:", response.data);

            // Update local state
            setGroup(prev => ({
                ...prev,
                assignments: [...prev.assignments, {
                    ...response.data,
                    tasks_count: 0,
                    user_completed_tasks_count: 0
                }]
            }));

            // Reset form and close modal
            setIsCreateAssignmentModalVisible(false);
            assignmentForm.resetFields();
            message.success('Assignment created successfully!');

        } catch (error) {
            console.error("Full error details:", error);

            let errorMessage = "Failed to create assignment";

            if (error.response) {
                // Server responded with error status
                console.error("Server response:", error.response.data);
                console.error("Status code:", error.response.status);

                if (error.response.status === 500) {
                    errorMessage = "Server error occurred. Please try again later.";
                } else if (error.response.data) {
                    // Try to extract meaningful error message
                    if (typeof error.response.data === 'string') {
                        errorMessage = error.response.data;
                    } else if (error.response.data.detail) {
                        errorMessage = typeof error.response.data.detail === 'string'
                            ? error.response.data.detail
                            : JSON.stringify(error.response.data.detail);
                    }
                }
            } else if (error.request) {
                // Request was made but no response received
                console.error("No response received:", error.request);
                errorMessage = "No response from server. Check your connection.";
            } else {
                // Other errors
                console.error("Request setup error:", error.message);
                errorMessage = error.message;
            }

            message.error(errorMessage);
        }
    };

    if (loading) return <div>Загрузка информации о группе...</div>;
    if (error) return <div>Ошибка: {error}</div>;
    if (!group) return <div>Группа не найдена</div>;

    return (
        <div style={{ padding: '24px' }}>
            <Card>
                <Title level={2}>{group.title}</Title>
                <Paragraph>{group.description}</Paragraph>

                <Space style={{ marginBottom: '16px' }}>
                    {(userRole === 0 || userRole === 1) && (
                        <>
                            <Button
                                type="primary"
                                onClick={() => setIsInviteSettingsModalVisible(true)}
                                icon={<PlusOutlined />}
                            >
                                Пригласить участников
                            </Button>
                            <Button
                                icon={<EditOutlined />}
                                onClick={showEditModal}
                            >
                                Редактировать группу
                            </Button>
                        </>
                    )}
                    {userRole === 0 && (
                        <Popconfirm
                            title={`Вы уверены, что хотите удалить группу "${group.title}"? Это действие нельзя отменить!`}
                            onConfirm={handleDeleteGroup}
                            okText="Да, удалить"
                            cancelText="Отмена"
                            okButtonProps={{ danger: true }}
                        >
                            <Button danger icon={<CloseOutlined />}>
                                Удалить группу
                            </Button>
                        </Popconfirm>
                    )}
                    <Popconfirm
                        title={`Вы уверены, что хотите покинуть группу "${group.title}"?`}
                        onConfirm={handleLeaveGroup}
                        okText="Да"
                        cancelText="Нет"
                    >
                        <Button danger icon={<LogoutOutlined />}>
                            Покинуть группу
                        </Button>
                    </Popconfirm>
                </Space>

                <Divider />

                <Title level={4}>Участники:</Title>
                <List
                    dataSource={group.accounts}
                    renderItem={account => (
                        <List.Item
                            actions={
                                userRole === 0 ? [
                                    account.role === 2 ? (
                                        <Popconfirm
                                            title="Повысить этого пользователя до учителя?"
                                            onConfirm={() => handlePromoteToTeacher(account.user_id)}
                                            okText="Да"
                                            cancelText="Нет"
                                        >
                                            <Button
                                                type="text"
                                                style={{ color: '#52c41a' }}
                                                icon={<ArrowUpOutlined />}
                                                size="small"
                                            />
                                        </Popconfirm>
                                    ) : account.role === 1 ? (
                                        <Popconfirm
                                            title="Понизить этого пользователя до ученика?"
                                            onConfirm={() => handleDemoteToStudent(account.user_id)}
                                            okText="Да"
                                            cancelText="Нет"
                                        >
                                            <Button
                                                type="text"
                                                danger
                                                icon={<ArrowDownOutlined />}
                                                size="small"
                                            />
                                        </Popconfirm>
                                    ) : null,
                                    account.role === 2 && (
                                        <Popconfirm
                                            title="Вы уверены, что хотите удалить этого пользователя из группы?"
                                            onConfirm={() => handleRemoveUser(account.user_id)}
                                            okText="Да"
                                            cancelText="Нет"
                                        >
                                            <Button
                                                type="text"
                                                danger
                                                icon={<CloseOutlined />}
                                                size="small"
                                            />
                                        </Popconfirm>
                                    )
                                ] : []
                            }
                        >
                            <List.Item.Meta
                                avatar={<Avatar>{account.user_id}</Avatar>}
                                title={`user${account.user_id}`}
                                description={
                                    <Tag color={
                                        account.role === 0 ? 'red' :
                                        account.role === 1 ? 'orange' : 'green'
                                    }>
                                        {getRoleName(account.role)}
                                    </Tag>
                                }
                            />
                        </List.Item>
                    )}
                />

                <Divider />

                <Row justify="space-between" align="middle" style={{ marginBottom: 16 }}>
                    <Title level={4} style={{ margin: 0 }}>Модули:</Title>
                    {(userRole === 0 || userRole === 1) && (
                        <Button
                            type="primary"
                            icon={<PlusOutlined />}
                            onClick={() => setIsCreateAssignmentModalVisible(true)}
                        >
                            Создать модуль
                        </Button>
                    )}
                </Row>

                <List
                    dataSource={group.assignments}
                    renderItem={assignment => (
                        <List.Item>
                            <Card
                                size="small"
                                title={assignment.title}
                                style={{ width: '100%' }}
                                extra={
                                    <Tag color={assignment.is_contest ? 'purple': 'transparent'}>
                                        {assignment.is_contest ? 'Контест': ''}
                                    </Tag>
                                }
                                hoverable
                                onClick={() => handleAssignmentClick(assignment.id)}
                            >
                                <Text>
                                    Выполнено: {assignment.user_completed_tasks_count} из {assignment.tasks_count} задач
                                </Text>
                            </Card>
                        </List.Item>
                    )}
                />
            </Card>

            {/* Модальное окно настроек приглашения */}
            <Modal
                title="Настройки приглашения"
                open={isInviteSettingsModalVisible}
                onOk={handleGenerateInviteLink}
                onCancel={() => setIsInviteSettingsModalVisible(false)}
                okText="Сгенерировать ссылку"
                cancelText="Отмена"
            >
                <Form layout="vertical">
                    <Form.Item label="Тип приглашения">
                        <Select
                            value={inviteType}
                            onChange={setInviteType}
                        >
                            <Option value="single_use">Одноразовое</Option>
                            <Option value="multi_use">Многоразовое</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item label="Срок действия (минуты)">
                        <InputNumber
                            min={5}
                            max={10080}
                            value={expiresMinutes}
                            onChange={setExpiresMinutes}
                            style={{ width: '100%' }}
                        />
                    </Form.Item>
                    <Alert
                        message="Информация"
                        description="Ссылка будет действительна только в течение указанного времени. После истечения срока действия потребуется создать новую ссылку."
                        type="info"
                        showIcon
                        icon={<InfoCircleOutlined />}
                    />
                </Form>
            </Modal>

            {/* Модальное окно ссылки для вступления */}
            <Modal
                title="Ссылка для вступления в группу"
                open={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={[
                    <Button
                        key="copy"
                        icon={<CopyOutlined />}
                        onClick={copyToClipboard}
                        type="primary"
                    >
                        Скопировать ссылку
                    </Button>,
                    <Button
                        key="close"
                        onClick={() => setIsModalVisible(false)}
                    >
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
                    description="Отправьте эту ссылку пользователям, которых вы хотите добавить в группу. После перехода по ссылке они автоматически станут участниками группы."
                    type="info"
                    showIcon
                    style={{ marginTop: 16 }}
                />
            </Modal>

            {/* Модальное окно редактирования группы */}
            <Modal
                title="Редактирование группы"
                open={isEditModalVisible}
                onOk={handleEditSubmit}
                onCancel={() => setIsEditModalVisible(false)}
                okText="Сохранить"
                cancelText="Отмена"
            >
                <Form form={form} layout="vertical">
                    <Form.Item
                        name="title"
                        label="Название группы"
                        rules={[{ required: true, message: 'Пожалуйста, введите название группы' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="description"
                        label="Описание группы"
                    >
                        <TextArea rows={4} />
                    </Form.Item>
                </Form>
            </Modal>
            <Modal
                title="Создание нового модуля"
                open={isCreateAssignmentModalVisible}
                onOk={handleCreateAssignment}
                onCancel={() => setIsCreateAssignmentModalVisible(false)}
                okText="Создать"
                cancelText="Отмена"
                width={700}
            >
                <Form form={assignmentForm} layout="vertical">
                    <Form.Item
                        name="title"
                        label="Название модуля"
                        rules={[{ required: true, message: 'Пожалуйста, введите название модуля' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="description"
                        label="Описание модуля"
                    >
                        <TextArea rows={4} />
                    </Form.Item>
                    <Form.Item
                        name="is_contest"
                        label="Это контест?"
                        valuePropName="checked"
                    >
                        <Switch />
                    </Form.Item>
                    <Form.Item
                        name="dateRange"
                        label="Период активности"
                        rules={[{ required: true, message: 'Пожалуйста, выберите период активности' }]}
                    >
                        <RangePicker
                            showTime
                            format="YYYY-MM-DD HH:mm:ss"
                            style={{ width: '100%' }}
                        />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default GroupDetails;