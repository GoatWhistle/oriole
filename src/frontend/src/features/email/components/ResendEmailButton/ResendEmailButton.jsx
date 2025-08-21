import React, { useState } from 'react';
import { handleResendEmail } from '../../handlers/user.jsx';
import styles from './ResendEmailButton.module.css';

const ResendEmailButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    const { success, error } = await handleResendEmail();

    if (success) {
      setSuccess(true);
    } else {
      setError(error);
    }

    setIsLoading(false);
  };

  return (
    <div>
      <button
        className={styles.button}
        onClick={handleClick}
        disabled={isLoading}
      >
        {isLoading ? 'Отправка...' : 'Отправить письмо повторно'}
      </button>

      {error && <div className={styles.error}>{error}</div>}
      {success && <div className={styles.success}>Письмо успешно отправлено!</div>}
    </div>
  );
};

export default ResendEmailButton;
