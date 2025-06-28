import { login, forgotPassword } from '../api/user.jsx';
import { fetchError } from '../../api/error.jsx';

export const handleLogin = async (values, navigate, setLoading) => {
  try {
    setLoading(true);
    const response = await login(values.email, values.password);

    if (response.access_token) {
      navigate('/');
      return true;
    }
    throw new Error('Токен не получен');
  } catch (error) {
      fetchError(error, `Ошибка сервера: ${error.response.status}`);
  } finally {
    setLoading(false);
  }
};

export const handleForgotPassword = async (email, setLoading) => {
  try {
    if (!email) {
      return false;
    }

    setLoading(true);
    const response = await forgotPassword(email);
    return true;
  } catch (error) {
      fetchError(error, error.response.data?.detail || 'Ошибка сервера');
  } finally {
    setLoading(false);
  }
};