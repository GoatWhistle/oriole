import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';
import { useNavigate } from 'react-router-dom';

const AssignmentMenu = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [assignments, setAssignments] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserAssignments = async () => {
            try {
                const response = await fetch('/api/v1/assignments/');

                if (!response.ok) {
                    throw new Error('Для отображения работ войдите в аккаунт');
                }

                const data = await response.json();

                if (data.length === 0) {
                    setAssignments([{
                        key: 'no-assignments',
                        label: 'У вас пока нет заданий',
                        disabled: true
                    }]);
                } else {
                    const menuItems = data.map(assignment => ({
                        key: assignment.id,
                        label: assignment.title,
                        title: assignment.description
                    }));
                    setAssignments(menuItems);
                }

                setLoading(false);
            } catch (err) {
                setError(err.message);
                console.error('Ошибка:', err);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchUserAssignments();
    }, []);

    const onClick = (e) => {
        if (e.key !== 'no-assignments') {
            navigate(`/assignments/${e.key}`);
        }
    };

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <Menu
            onClick={onClick}
            style={{ width: 250 }}
            mode="inline"
            items={assignments}
        />
    );
};

export default AssignmentMenu;