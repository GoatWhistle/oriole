import React from 'react';
import Header from "/src/features/components/Header/Header.jsx";
import GroupList from "/src/features/groups/components/GroupList/GroupList.jsx";
import ModuleList from "/src/features/modules/components/ModuleList/ModuleList.jsx";
import CreateGroupButton from "/src/features/groups/components/CreateGroupButton/CreateGroupButton.jsx";
import myGif from "../presets/oriole-footer.gif";

import { Card, Typography } from 'antd';
const { Title } = Typography;

export default function Home() {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />
      <div style={{
        maxWidth: 1200,
        margin: '0 auto',
        padding: '150px'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '40px',
          flexWrap: 'wrap'
        }}>
          <GroupList />
          <ModuleList />
          <CreateGroupButton />
          <img
            src={myGif}
            alt="Описание гифки"
            style={{ width: '300px', height: 'auto' }}
          />
        </div>
      </div>
    </div>
  );
}
