import axios from 'axios';

export const promoteUser = async (groupId, userId) => {
  await axios.patch(`/api/groups/${groupId}/promote/${userId}/`);
};

export const demoteUser = async (groupId, userId) => {
  await axios.patch(`/api/groups/${groupId}/demote/${userId}/`);
};

export const kickUser = async (groupId, userId) => {
  await axios.delete(`/api/groups/${groupId}/kick/${userId}/`);
};

TODO: Figure out how to visualize user groups more effective
export const showGroupList = async () => {
  const response = await axios.get('/api/groups/?page=1&per_page=10');
  return await response.data;
};

