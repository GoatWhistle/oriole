import { login, forgotPassword, register, authViaTelegram } from '../api/user.jsx';
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

export const handleRegister = async (values, navigate, setLoading) => {
  try {
    setLoading(true);
    const userData = {
      email: values.email,
      password: values.password,
      name: values.firstName,
      surname: values.lastName,
      patronymic: values.middleName || '',
      is_active: true,
      is_superuser: false,
      is_verified: false
    };

    await register(userData);
    navigate('/login');
    return true;
  } catch (error) {
      fetchError(error, `Ошибка сервера: ${error.response.status}`);
  } finally {
    setLoading(false);
  }
};

export const handleAuthViaTelegram = async (setLoading) => {
  try {
    setLoading(true);
    const response = await authViaTelegram();

    if (response) {
      return true;
    }
  } catch (error) {
      fetchError(error, `Не удалось войти через Telegram`);
  } finally {
    setLoading(false);
  }
};