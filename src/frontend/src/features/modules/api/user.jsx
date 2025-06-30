import axios from 'axios';

export const showModuleList = async () => {
  const response = await axios.get('/api/modules/');
  return await response.data;
};
