import { forgotPassword, resetPassword } from '../api/user.jsx';
import { fetchError } from '../../api/error.jsx';

export const handleForgotPassword = async (token, newPassword, navigate, setLoading) => {
  try {
    setLoading(true);
    const response = await forgotPassword(token, newPassword);

    if (response.status === 'success') {
      navigate('/');
      return true;
    }
  } catch (error) {
      fetchError(error, 'Ошибка при восстановлении пароля');
  } finally {
    setLoading(false);
  }
};

export const handleResetPassword = async (token, newPassword, navigate, setLoading) => {
  try {
    setLoading(true);
    const response = await resetPassword(token, newPassword);

    if (response.status === 'success') {
      navigate('/');
      return true;
    }
  } catch (error) {
      fetchError(error, error.response ? 'Ошибка сервера' : 'Ошибка сети');
  } finally {
      setLoading(false);
  }
};