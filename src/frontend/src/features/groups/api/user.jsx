import axios from 'axios';

export const promoteUser = async (spaceId, userId) => {
  await axios.patch(`/api/spaces/${spaceId}/promote/${userId}/`);
};

export const demoteUser = async (spaceId, userId) => {
  await axios.patch(`/api/spaces/${spaceId}/demote/${userId}/`);
};

export const kickUser = async (spaceId, userId) => {
  await axios.delete(`/api/spaces/${spaceId}/kick/${userId}/`);
};

/* Figure out how to visualize user groups more effective */
export const showGroupList = async () => {
  const response = await axios.get('/api/groups/?page=1&per_page=10');
  return await response.data;
};

