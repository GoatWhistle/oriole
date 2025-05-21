import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Typography, Divider, Progress, List, message } from 'antd';

const { Title, Text, Paragraph } = Typography;

const AssignmentDetails = () => {
    const { assignment_id } = useParams();
    const [assignment, setAssignment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAssignment = async () => {
            try {
                const response = await fetch(`/api/v1/assignments/${assignment_id}/`);

                if (!response.ok) {
                    throw new Error('Не удалось загрузить информацию о задании');
                }

                const data = await response.json();
                setAssignment(data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchAssignment();
    }, [assignment_id]);

    if (loading) return <div>Загрузка задания...</div>;
    if (error) return <div>Ошибка: {error}</div>;
    if (!assignment) return <div>Задание не найдено</div>;

    const completionPercentage = assignment.tasks_count > 0
        ? Math.round((assignment.user_completed_tasks_count / assignment.tasks_count) * 100)
        : 0;

    return (
        <div style={{ padding: '24px' }}>
            <Card>
                <Title level={2}>{assignment.title}</Title>
                <Paragraph>{assignment.description}</Paragraph>

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
                                    task.is_correct ?
                                        <Text type="success">Выполнено</Text> :
                                        <Text type="warning">В процессе</Text>
                                }
                            >
                                <Paragraph>{task.description}</Paragraph>
                                <Text type={task.is_active ? 'success' : 'danger'}>
                                    {task.is_active ? 'Активна' : 'Неактивна'}
                                </Text>
                            </Card>
                        </List.Item>
                    )}
                />
            </Card>
        </div>
    );
};

export default AssignmentDetails;