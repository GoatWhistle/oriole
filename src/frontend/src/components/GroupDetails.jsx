import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Typography, Divider, List, Avatar, Tag, message } from 'antd';

const { Title, Text, Paragraph } = Typography;

const GroupDetails = () => {
    const { group_id } = useParams();
    const navigate = useNavigate();
    const [group, setGroup] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchGroup = async () => {
            try {
                const response = await fetch(`/api/v1/learn/groups/${group_id}/`);

                if (!response.ok) {
                    throw new Error('Не удалось загрузить информацию о группе');
                }

                const data = await response.json();
                setGroup(data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchGroup();
    }, [group_id]);

    if (loading) return <div>Загрузка информации о группе...</div>;
    if (error) return <div>Ошибка: {error}</div>;
    if (!group) return <div>Группа не найдена</div>;

    const getRoleName = (role) => {
        switch(role) {
            case 0: return 'Ученик';
            case 1: return 'Учитель';
            case 2: return 'Администратор';
            default: return 'Неизвестная роль';
        }
    };

    const handleAssignmentClick = (assignmentId) => {
        navigate(`/assignment/${assignmentId}`);
    };

    return (
        <div style={{ padding: '24px' }}>
            <Card>
                <Title level={2}>{group.title}</Title>
                <Paragraph>{group.description}</Paragraph>

                <Divider />

                <Title level={4}>Участники:</Title>
                <List
                    dataSource={group.accounts}
                    renderItem={account => (
                        <List.Item>
                            <List.Item.Meta
                                avatar={<Avatar>{account.user_id}</Avatar>}
                                title={`user${account.user_id}`}
                                description={
                                    <Tag color={
                                        account.role === 0 ? 'green' :
                                        account.role === 1 ? 'orange' : 'red'
                                    }>
                                        {getRoleName(account.role)}
                                    </Tag>
                                }
                            />
                        </List.Item>
                    )}
                />

                <Divider />

                <Title level={4}>Модули:</Title>
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
                            </Card>
                        </List.Item>
                    )}
                />
            </Card>
        </div>
    );
};

export default GroupDetails;