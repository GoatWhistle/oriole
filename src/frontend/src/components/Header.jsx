import {Card} from "antd";
import orioleIcon from './oriole-icon.png';

function Header() {

  return (
    <>
    <Card
        title={
            <div className="flex items-center gap-2">
                <img src={orioleIcon} alt="Oriole Icon" width="80" height="80" />
                <div className="gap-10 flex items-center">
                    <span style={{ fontSize: '30px' }}> Oriole </span>
                    <div className="flex gap-5">
                        <MenuButton/>
                    </div>
                </div>
            </div>
        }
        extra={
                        <a href="#" style={{ fontSize: '20px' }}>Войти</a>
              }
        style={{ width: '100%', height: 0, margin: 0 }}
    >
    </Card>
    </>
  )
}

export default Header
