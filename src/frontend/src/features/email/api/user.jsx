import axios from 'axios';

export const forgotPassword = async (token, newPassword) => {
  const response = await axios.get(
    `/api/verify/forgot_password_redirect/${token}`,
    {
      params: { new_password: newPassword },
      withCredentials: true
    }
  );
  return response.data;
};

export const resetPassword = async (token, newPassword) => {
  const response = await axios.get(
    `/api/verify/reset_password_redirect/${token}`,
    {
      params: { new_password: newPassword },
      withCredentials: true
    }
  );
  return response.data;
};