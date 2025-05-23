import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Col
} from 'antd';
import {
  CopyOutlined,
  CloseOutlined,
  EditOutlined,
  LogoutOutlined,
  PlusOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { RangePicker } = DatePicker;

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
    const [form] = Form.useForm();
    const [assignmentForm] = Form.useForm();
    const [userTimezone, setUserTimezone] = useState('UTC');

    useEffect(() => {
        const detectTimezone = () => {
            try {
                const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
                return timezone || 'UTC';
            } catch (e) {
                return 'UTC';
            }
        };

        const fetchData = async () => {
            try {
                setUserTimezone(detectTimezone());

                const groupResponse = await fetch(`/api/v1/learn/groups/${group_id}/`);
                if (!groupResponse.ok) {
                    throw new Error('Не удалось загрузить информацию о группе');
                }
                const groupData = await groupResponse.json();
                setGroup(groupData);

                const roleResponse = await fetch(`/api/v1/users/get-role/group/${group_id}/`);
                if (!roleResponse.ok) {
                    throw new Error('Не удалось определить вашу роль в группе');
                }
                const roleData = await roleResponse.json();
                setUserRole(roleData);

                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchData();
    }, [group_id]);

    const handleGenerateInviteLink = async () => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/invite/`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Не удалось сгенерировать ссылку для вступления');
            }

            const data = await response.json();
            setInviteLink(data.link);
            setIsModalVisible(true);
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDeleteGroup = async () => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Не удалось удалить группу');
            }

            message.success('Группа успешно удалена');
            navigate('/groups');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handlePromoteToTeacher = async (userId) => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/promote/${userId}/`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                throw new Error('Не удалось повысить пользователя до учителя');
            }

            const updatedAccounts = group.accounts.map(account => {
                if (account.user_id === userId) {
                    return { ...account, role: 1 };
                }
                return account;
            });

            setGroup({
                ...group,
                accounts: updatedAccounts
            });

            message.success('Пользователь успешно повышен до учителя');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleDemoteToStudent = async (userId) => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/demote/${userId}/`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                throw new Error('Не удалось понизить пользователя до ученика');
            }

            const updatedAccounts = group.accounts.map(account => {
                if (account.user_id === userId) {
                    return { ...account, role: 2 };
                }
                return account;
            });

            setGroup({
                ...group,
                accounts: updatedAccounts
            });

            message.success('Пользователь понижен до ученика');
        } catch (err) {
            message.error(err.message);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(inviteLink);
        message.success('Ссылка скопирована в буфер обмена');
    };

    const getRoleName = (role) => {
        switch(role) {
            case 0: return 'Создатель';
            case 1: return 'Учитель';
            case 2: return 'Ученик';
            default: return 'Неизвестная роль';
        }
    };

    const handleAssignmentClick = (assignmentId) => {
        navigate(`/assignment/${assignmentId}`);
    };

    const handleRemoveUser = async (removeUserId) => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/kick/${removeUserId}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Не удалось удалить пользователя из группы');
            }

            const updatedAccounts = group.accounts.filter(account => account.user_id !== removeUserId);
            setGroup({
                ...group,
                accounts: updatedAccounts
            });

            message.success('Пользователь успешно удален из группы');
        } catch (err) {
            message.error(err.message);
        }
    };

    const handleLeaveGroup = async () => {
        try {
            const response = await fetch(`/api/v1/learn/groups/${group_id}/leave/`, {
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
            const response = await fetch(`/api/v1/learn/groups/${group_id}/`, {
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

            // Функция для преобразования даты в ISO формат
            const formatToISO = (momentDate) => {
                return momentDate.format('YYYY-MM-DDTHH:mm:ss');
            };

            const assignmentData = {
                title: values.title,
                description: values.description || "",
                is_contest: Boolean(values.is_contest),
                group_id: parseInt(group_id),
                start_datetime: formatToISO(values.dateRange[0]),
                end_datetime: formatToISO(values.dateRange[1])
            };

            const response = await fetch('/api/v1/assignments/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    assignment_in: assignmentData,
                    user_timezone: userTimezone
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || errorData.message || 'Не удалось создать модуль');
            }

            const newAssignment = await response.json();

            setGroup(prev => ({
                ...prev,
                assignments: [...prev.assignments, {
                    ...newAssignment,
                    tasks_count: 0,
                    user_completed_tasks_count: 0
                }]
            }));

            setIsCreateAssignmentModalVisible(false);
            assignmentForm.resetFields();
            message.success('Модуль успешно создан!');

        } catch (err) {
            console.error("Ошибка при создании модуля:", err);
            message.error(`Ошибка: ${err.message}`);
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
                                onClick={handleGenerateInviteLink}
                            >
                                Ссылка для вступления
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
                            title={`Вы уверены, что хотите полностью удалить группу "${group.title}"? Это действие нельзя отменить!`}
                            onConfirm={handleDeleteGroup}
                            okText="Да, удалить"
                            cancelText="Отмена"
                            okButtonProps={{ danger: true }}
                        >
                            <Button
                                danger
                                icon={<CloseOutlined />}
                            >
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
                        <Button
                            danger
                            icon={<LogoutOutlined />}
                        >
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
                                    <Tag color={assignment.is_contest ? 'purple' : 'green'}>
                                        {assignment.is_contest ? 'Контест' : 'Задание'}
                                    </Tag>
                                }
                                hoverable
                                onClick={() => handleAssignmentClick(assignment.id)}
                            >
                                <Text>
                                    Выполнено: {assignment.user_completed_tasks_count} из {assignment.tasks_count} задач
                                </Text>
                                <div style={{ marginTop: 8 }}>
                                    <Text type="secondary">
                                        {new Date(assignment.start_datetime).toLocaleString()} - {new Date(assignment.end_datetime).toLocaleString()}
                                    </Text>
                                </div>
                            </Card>
                        </List.Item>
                    )}
                />
            </Card>

            <Modal
                title="Ссылка для вступления в группу"
                visible={isModalVisible}
                onCancel={() => setIsModalVisible(false)}
                footer={[
                    <Button
                        key="copy"
                        icon={<CopyOutlined />}
                        onClick={copyToClipboard}
                    >
                        Скопировать
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
                />
                <Text type="secondary" style={{ marginTop: '8px', display: 'block' }}>
                    Отправьте эту ссылку ученикам для вступления в группу
                </Text>
            </Modal>

            <Modal
                title="Редактирование группы"
                visible={isEditModalVisible}
                onOk={handleEditSubmit}
                onCancel={() => setIsEditModalVisible(false)}
                okText="Сохранить"
                cancelText="Отмена"
            >
                <Form
                    form={form}
                    layout="vertical"
                >
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
                        <Input.TextArea rows={4} />
                    </Form.Item>
                </Form>
            </Modal>

            <Modal
                title="Создание нового модуля"
                visible={isCreateAssignmentModalVisible}
                onOk={handleCreateAssignment}
                onCancel={() => setIsCreateAssignmentModalVisible(false)}
                okText="Создать"
                cancelText="Отмена"
                width={700}
            >
                <Form
                    form={assignmentForm}
                    layout="vertical"
                >
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
                        label="Часовой пояс (автоматически определен)"
                    >
                        <Input value={userTimezone} readOnly />
                    </Form.Item>
                    <Form.Item
                        name="dateRange"
                        label="Период активности"
                        rules={[{ required: true, message: 'Пожалуйста, выберите период активности' }]}
                    >
                        <RangePicker
                            showTime
                            format="YYYY-MM-DD HH:mm"
                            style={{ width: '100%' }}
                        />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default GroupDetails;