import React, { useState, useEffect } from 'react';
import { Menu, message } from 'antd';
import { useNavigate } from 'react-router-dom';

const ModuleMenu = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [modules, setModules] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserModules = async () => {
            try {
                const response = await fetch('/api/modules/');

                if (!response.ok) {
                    throw new Error('Для отображения работ войдите в аккаунт');
                }

                const data = await response.json();

                if (data.length === 0) {
                    setModules([{
                        key: 'no-modules',
                        label: 'У вас пока нет заданий',
                        disabled: true
                    }]);
                } else {
                    const menuItems = data.map(module => ({
                        key: module.id,
                        label: module.title,
                        title: module.description
                    }));
                    setModules(menuItems);
                }

                setLoading(false);
            } catch (err) {
                setError(err.message);
                console.error('Ошибка:', err);
                setLoading(false);
                message.error(err.message);
            }
        };

        fetchUserModules();
    }, []);

    const onClick = (e) => {
        if (e.key !== 'no-modules') {
            navigate(`/modules/${e.key}`);
        }
    };

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <Menu
            onClick={onClick}
            style={{ width: 250 }}
            mode="inline"
            items={modules}
        />
    );
};

export default ModuleMenu;