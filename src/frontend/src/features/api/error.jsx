import { message } from 'antd';

export const fetchError = (error, defaultMessage) => {
  console.error(error);
  const errorMessage = error.response?.data?.detail || error.message || defaultMessage;
  message.error(errorMessage);
  throw new Error(errorMessage);
};