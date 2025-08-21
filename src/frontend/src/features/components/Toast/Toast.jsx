import React from 'react';
import { fetchToast } from '../../api/toast.jsx';
import styles from './Toast.module.css';

const Toast = ({ type, title, description }) => {
  const toastData = fetchToast(type, title, description);

  const containerClass = `${styles.container} ${styles[`container_${toastData.type}`]}`;
  const dividerClass = `${styles.divider} ${styles[`divider_${toastData.type}`]}`;

  return (
    <div className={containerClass}>
      <div className={styles.header}>
        {toastData.getIcon()}
        {toastData.title}
      </div>
      <div className={dividerClass} />
      <div className={styles.description}>{toastData.description}</div>
    </div>
  );
};

export default Toast;