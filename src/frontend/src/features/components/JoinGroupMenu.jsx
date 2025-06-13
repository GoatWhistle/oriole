import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Typography, Button, Result, Spin, message } from 'antd';
import axios from 'axios';

const { Title, Text } = Typography;

const JoinGroupMenu = () => {
    const { invite_code } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const joinGroup = async () => {
            try {
                setLoading(true);
                const response = await axios.post(`/api/groups/join/${invite_code}`, {}, {
                    withCredentials: true
                });

                setResult(response.data);
                message.success('Вы успешно вступили в группу!');
            } catch (err) {
                console.error('Ошибка вступления в группу:', err);
                setError(err.response?.data?.detail || 'Не удалось вступить в группу');
                message.error(err.response?.data?.detail || 'Не удалось вступить в группу');
            } finally {
                setLoading(false);
            }
        };

        joinGroup();
    }, [invite_code]);

    const handleNavigateToGroup = () => {
        if (result?.group_id) {
            navigate(`/groups/${result.group_id}`);
        } else {
            navigate('/');
        }
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <Spin size="large" tip="Обработка приглашения..." />
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: '24px' }}>
                <Card>
                    <Result
                        status="error"
                        title="Ошибка вступления в группу"
                        subTitle={error}
                        extra={[
                            <Button type="primary" key="home" onClick={() => navigate('/')}>
                                На главную
                            </Button>
                        ]}
                    />
                </Card>
            </div>
        );
    }

    return (
        <div style={{ padding: '24px' }}>
            <Card>
                <Result
                    status="success"
                    title="Вы вступили в группу!"
                    subTitle={
                        <Text>
                            Теперь вы участник группы. Можете перейти к просмотру заданий и участников.
                        </Text>
                    }
                    extra={[
                        <Button
                            type="primary"
                            key="group"
                            onClick={handleNavigateToGroup}
                        >
                            Перейти в группу
                        </Button>,
                        <Button key="home" onClick={() => navigate('/')}>
                            На главную
                        </Button>
                    ]}
                />
            </Card>
        </div>
    );
};

export default JoinGroupMenu;
