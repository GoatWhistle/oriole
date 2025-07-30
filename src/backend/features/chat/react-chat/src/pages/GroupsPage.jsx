import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken } from '../utils/auth';
import { getMe } from '../api/auth';
import { fetchGroups } from '../api/groups';

const GroupsPage = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadGroups = async () => {
      try {
        const token = getToken();
        const groupData = await fetchGroups(token);
        setGroups(groupData);
      } catch (err) {
        console.error("Ошибка загрузки групп", err);
      } finally {
        setLoading(false);
      }
    };

    loadGroups();
  }, []);

  const handleGroupClick = async (groupId) => {
    const token = getToken();
    const me = await getMe(token);
    navigate(`/chat?group_id=${groupId}&user_id=${me.id}`);
  };

  return (
    <div style={{ padding: "40px", background: "#fafafa", fontFamily: "Arial, sans-serif" }}>
      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>Выберите группу</h2>
      <div style={{ maxWidth: "500px", margin: "0 auto" }}>
        {loading ? (
          <p>Загрузка групп...</p>
        ) : groups.length === 0 ? (
          <p>У вас нет групп</p>
        ) : (
          groups.map((group) => (
            <div key={group.id} style={{ marginBottom: "15px" }}>
              <button
                style={{
                  backgroundColor: "#52c41a",
                  color: "white",
                  border: "none",
                  padding: "10px 16px",
                  borderRadius: "6px",
                  cursor: "pointer",
                  width: "100%",
                  fontSize: "16px",
                  fontWeight: "bold"
                }}
                onClick={() => handleGroupClick(group.id)}
              >
                {group.name || `Группа ${group.id}`}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default GroupsPage;
