import axios from 'axios';

export const fetchUserRole = async (groupId) => {
  const response = await axios.get(`/api/users/get-role/group/${groupId}/`);
  return response.data;
};
