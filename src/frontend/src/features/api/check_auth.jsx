import axios from 'axios';

export const fetchCheckAuth = async () => {
  try {
    const response = await axios.get('/api/333/auth/check-auth', {
        headers: {
            'accept': 'application/json',
        },
        withCredentials: true
    });
    return response;
  } catch (error) {
    console.error('Ошибка проверки авторизации:', error);
    return false;
  }
};