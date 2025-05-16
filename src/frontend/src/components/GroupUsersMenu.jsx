import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';

const GroupUsersMenu = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [groupUsers, setGroupUsers] = useState([]);
    const userId = useParams();

    useEffect(() => {
        const fetchGroupUsers = async () => {
            try {
                const response = await fetch(`/api/v1/learn/groups/${userId}/users/`);

                if (!response.ok) {
                    throw new Error('Ошибка отображения пользователей группы');
                }

                const data = await response.json();

                if (data.length === 0) {
                    setUserGroups([{
                        key: 'no-users',
                        label: 'В группе пока нет пользователей',
                        disabled: true
                    }]);
                } else {
                    const menuItems = data.map(user => ({
                        key: user.id,
                        label: group.name
                    }));
                    setGroupUsers(menuItems);
                }

                setLoading(false);
            } catch (err) {
                setError(err.message);
                console.error('Ошибка:', err);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchGroupUsers();
    }, []);

    const onClick = (e) => {
        if (e.key !== 'no-users') {
            console.log('Выбран пользователь с ID:', e.key);
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
            items={groupUsers}
        />
    );
};

export default GroupUsersMenu;