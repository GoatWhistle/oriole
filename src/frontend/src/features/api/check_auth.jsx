import axios from 'axios';

export const fetchCheckAuth = async () => {
  try {
    const response = await axios.get('/api/auth/check-auth', {
      headers: {
        'accept': 'application/json',
      },
      withCredentials: true
    });

    // Возвращаем данные пользователя при успешной аутентификации
    return {
      isAuthenticated: true,
      userData: response.data
    };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Сервер ответил с кодом ошибки (4xx, 5xx)
        console.error('Ошибка проверки авторизации:', error.response.data);
      } else {
        // Запрос был сделан, но ответ не получен
        console.error('Ошибка сети при проверке авторизации:', error.message);
      }
    } else {
      // Неожиданная ошибка
      console.error('Неожиданная ошибка при проверке авторизации:', error);
    }

    // Возвращаем объект с флагом аутентификации
    return {
      isAuthenticated: false,
      userData: null
    };
  }
};