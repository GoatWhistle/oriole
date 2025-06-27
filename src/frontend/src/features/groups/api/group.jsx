import axios from 'axios';

export const createGroup = async (groupData) => {
    const response = await axios.post('api/groups/', groupData, {
      withCredentials: true,
    });
    return response.data;
};

export const fetchGroup = async (groupId) => {
  const response = await axios.get(`/api/groups/${groupId}/`);
  return response.data;
};

export const leaveGroup = async (groupId) => {
  await axios.delete(`/api/groups/${groupId}/leave/`);
};

export const updateGroup = async (groupId, data) => {
  const response = await axios.patch(`/api/groups/${groupId}/`, data);
  return response.data;
};

export const deleteGroup = async (groupId) => {
  await axios.delete(`/api/groups/${groupId}/`);
};
