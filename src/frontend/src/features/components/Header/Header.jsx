import { Link } from 'react-router-dom';
import { useEffect } from 'react';

import orioleIcon from '../../presets/oriole-icon.png';
import AuthButton from '../AuthButton/AuthButton.jsx';

import styles from './Header.module.css';


function Header() {
  useEffect(() => {
    document.title = 'Oriole';
  });

  return (
    <div
      className={styles.headerCard}
    >
      <div className={styles.headerContainer}>
        <div className={styles.logoContainer}>
          <Link
            to="/"
            className={styles.logoLink}
          >
            <img className={styles.image} src={orioleIcon} alt="Oriole Icon" width="80" height="80" />
            <span className={styles.logoText}>Oriole</span>
          </Link>
        </div>

        <div className={styles.authButtonContainer}>
          <AuthButton />
        </div>
      </div>
    </div>
  )
}

export default Header
