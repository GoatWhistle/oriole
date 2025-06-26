import React from 'react';
import Header from "/src/features/components/Header/Header.jsx";
import GroupMenu from "/src/features/components/GroupMenu.jsx";
import ModuleMenu from "/src/features/components/ModuleMenu.jsx";
import CreateGroupButton from "/src/features/groups/components/CreateGroupButton/CreateGroupButton.jsx";

import { Card, Typography } from 'antd';
const { Title } = Typography;

export default function Home() {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />
      <div style={{
        maxWidth: 1200,
        margin: '0 auto',
        padding: '20px'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '40px',
          flexWrap: 'wrap'
        }}>
          <div style={{ width: 350 }}>
            <Card
              title={<span style={{ fontSize: '18px' }}>Мои группы</span>}
              bordered={false}
              style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
            >
              <GroupMenu />
            </Card>
          </div>

          <div style={{ width: 350 }}>
            <Card
              title={<span style={{ fontSize: '18px' }}>Мои модули</span>}
              bordered={false}
              style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
            >
              <ModuleMenu />
            </Card>
          </div>
          <CreateGroupButton />
        </div>
      </div>
    </div>
  );
}
