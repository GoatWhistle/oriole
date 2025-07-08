import axios from 'axios';

TODO: Figure out how to visualize user modules more effective
export const showModuleList = async () => {
  const response = await axios.get('/api/modules/?page=1&per_page=10');
  return await response.data;
};
