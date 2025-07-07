import { Card } from "antd";
import orioleIcon from './oriole-icon.png';
import { Link } from 'react-router-dom';
import { useEffect } from 'react';

import AuthButton from './AuthButton.jsx'

function Header() {

  useEffect(() => {
        document.title = 'Oriole';
      });

  return (
    <Card
      style={{ width: '100%' }}
      bodyStyle={{ padding: 0, display: 'flex', alignItems: 'center' }}
    >
      <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Link
              to="/"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                color: 'black',
                textDecoration: 'none'
              }}
            >
                <img src={orioleIcon} alt="Oriole Icon" width="80" height="80" />
                <span style={{ fontSize: '30px', color: 'black' }}>Oriole</span>
            </Link>
        </div>

        <AuthButton />

      </div>
    </Card>
  )
}

export default Header
