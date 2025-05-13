import { Card } from "antd";
import orioleIcon from './oriole-icon.png';
import MenuButton from "./MenuButton.jsx";
import { Link } from 'react-router-dom';

function Header() {
  return (
    <Card
      style={{ width: '100%' }}
      bodyStyle={{ padding: 0, display: 'flex', alignItems: 'center' }}
    >
      <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <img src={orioleIcon} alt="Oriole Icon" width="80" height="80" />
          <span style={{ fontSize: '30px' }}>Oriole</span>
        </div>

        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <MenuButton />
          <Link to="/login" style={{ fontSize: '20px' }}>Войти</Link>
        </div>
      </div>
    </Card>
  )
}

export default Header