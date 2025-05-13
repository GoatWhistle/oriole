import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';

const GroupMenu = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userGroups, setUserGroups] = useState([]); // Added state for userGroups

    useEffect(() => {
        fetch('/api/v1/learn/groups/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Войдите в аккаунт');
                }
                return response.json();
            })
            .then(data => {
                setUserGroups(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                console.error(err);
                setLoading(false);
            });
    }, []);

    const onClick = e => {
        console.log('click ', e);
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

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