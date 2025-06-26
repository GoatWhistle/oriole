import axios from 'axios';

export const fetchCheckAuth = async () => {
  try {
    const response = await axios.get('/api/auth/check-auth', {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка проверки авторизации:', error);
    return false;
  }
};