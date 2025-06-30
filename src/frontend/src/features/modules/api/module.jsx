import axios from 'axios';

export const createModule = async (moduleData) => {
  const response = await axios.post('/api/modules/', moduleData);
  return response.data;
};

export const getModule = async (module_id) => {
  const response = await axios.get(`/api/modules/${module_id}/`);
  return response.data;
};

export const getUserRole = async (group_id) => {
  const response = await axios.get(`/api/users/get-role/group/${group_id}`);
  return response.data;
};

export const createTask = async (taskData) => {
  const response = await axios.post('/api/tasks/', taskData);
  return response.data;
};

export const deleteModule = async (module_id) => {
  await axios.delete(`/api/modules/${module_id}/`);
};

export const updateModule = async (module_id, moduleData) => {
  const response = await axios.patch(`/api/modules/${module_id}/`, moduleData);
  return response.data;
};