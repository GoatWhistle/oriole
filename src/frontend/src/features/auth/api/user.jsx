import axios from 'axios';

export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await axios.post('/api/auth/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const forgotPassword = async (email) => {
  const response = await axios.post(
    `/api/auth/forgot_password?email=${encodeURIComponent(email)}`,
    null,
    {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    }
  );
  return response.data;
};

export const register = async (userData) => {
  const response = await axios.post('/api/auth/register', userData, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });
  return response.data;
};

export const authViaTelegram = async () => {
  const response = await axios.post('/api/auth-via-telegram/telegram');
  return response.data;
};