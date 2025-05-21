import React from 'react';
import Header from "/src/components/Header.jsx";
import GroupMenu from "/src/components/GroupMenu.jsx";
import AssignmentMenu from "/src/components/AssignmentMenu.jsx";
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
        <Title level={2} style={{ textAlign: 'center', margin: '24px 0' }}>
          Welcome to the Home Page
        </Title>

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
              <AssignmentMenu />
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}