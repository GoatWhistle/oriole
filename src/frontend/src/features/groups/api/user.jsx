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

export const showGroupList = async () => {
  const response = await fetch('/api/groups/');
  return await response.json();
};

