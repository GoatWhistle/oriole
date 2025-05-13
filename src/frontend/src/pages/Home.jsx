import React from 'react';
import Header from "/src/components/Header.jsx";
import GroupMenu from "/src/components/GroupMenu.jsx";
import AssignmentMenu from "/src/components/AssignmentMenu.jsx";

export default function Home() {
  return <div>
            <Header/>
            <h1>Welcome to the Home Page</h1>
            <div style={{ display: 'flex'}}>
                <GroupMenu />
                <AssignmentMenu />
            </div>
         </div>
}
