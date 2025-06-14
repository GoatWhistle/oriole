import axios from 'axios';

export const createModule = async (moduleData) => {
  const response = await axios.post('/api/modules/', moduleData);
  return response.data;
};