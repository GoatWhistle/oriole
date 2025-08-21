import axios from 'axios';

export const showUserProfile = async () => {
  const response = await axios.get('/api/auth/check-auth', {
    withCredentials: true
  });
  return response.data;
};

export const updateUserProfile = async (data) => {
  const response = await axios.patch(
    '/api/users/profile',
    data,
    { withCredentials: true }
  );
  return response.data;
};

export const resetPassword = async () => {
  const response = await axios.post(
    '/api/auth/reset_password',
    {},
    { withCredentials: true }
  );
  return response.data;
};

export const logoutUser = async () => {
  await axios.delete('/api/auth/logout', { withCredentials: true });
};

export const deleteUserAccount = async () => {
  await axios.delete('/api/users', { withCredentials: true });
};
