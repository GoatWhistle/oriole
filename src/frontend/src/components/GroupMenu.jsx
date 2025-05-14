import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';

const GroupMenu = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userGroups, setUserGroups] = useState([]);

    useEffect(() => {
        const fetchUserGroups = async () => {
            try {
                const response = await fetch('/api/v1/learn/groups/');

                if (!response.ok) {
                    throw new Error('Для отображения групп войдите в аккаунт');
                }

                const data = await response.json();

                if (data.length === 0) {
                    setUserGroups([{
                        key: 'no-groups',
                        label: 'У вас пока нет групп',
                        disabled: true
                    }]);
                } else {
                    const menuItems = data.map(group => ({
                        key: group.id,
                        label: group.title
                    }));
                    setUserGroups(menuItems);
                }

                setLoading(false);
            } catch (err) {
                setError(err.message);
                console.error('Ошибка:', err);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchUserGroups();
    }, []);

    const onClick = (e) => {
        if (e.key !== 'no-groups') {
            console.log('Выбрана группа с ID:', e.key);
            // Здесь можно добавить логику обработки выбора группы
        }
    };

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <Menu
            onClick={onClick}
            style={{ width: 200 }}
            mode="inline"
            items={userGroups}
        />
    );
};

export default GroupMenu;