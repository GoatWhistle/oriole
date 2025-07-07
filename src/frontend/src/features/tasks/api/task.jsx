import axios from 'axios';

export const getTask = async (task_id) => {
    const response = await axios.get(`/api/tasks/${task_id}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    return response.data;
};

export const tryToCompleteTask = async (task_id, user_answer) => {
    const response = await axios.patch(
      `/api/tasks/${task_id}/complete/?user_answer=${encodeURIComponent(user_answer)}`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'application/json'
        },
        withCredentials: true
      }
    );
    return response.data;
};

export const updateTask = async (task_id, taskData) => {
    const response = await axios.patch(
      `/api/tasks/${task_id}/`,
      taskData,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    );
    return response.data;
};

export const deleteTask = async (task_id) => {
    await axios.delete(`/api/tasks/${task_id}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
};
