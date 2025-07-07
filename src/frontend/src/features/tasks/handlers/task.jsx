import { fetchError } from '../../api/error.jsx'
import { fetchUserRole } from '../../api/user_role.jsx';

import {
  getTask,
  tryToCompleteTask,
  updateTask,
  deleteTask,
} from '../api/task.jsx';

export const handleGetTask = async (task_id, setTask, setLoading, setUserRole) => {
  try {
    setLoading(true);
    const taskData = await getTask(task_id);
    setTask(taskData);

    if (taskData.module_id) {
      const role = await fetchUserRole(taskData.group_id);
      if (role !== null) {
        setUserRole(role);
      }
    }

    return taskData;
  } catch (error) {
    fetchError(error, 'Не удалось загрузить информацию о группе')
  } finally {
    setLoading(false);
  }
};

export const handleTryToCompleteTask = async (task_id, user_answer, fetchTaskData) => {
  try {
    const result = await tryToCompleteTask(task_id, user_answer);
    await fetchTaskData();
    return result;
  } catch (error) {
    fetchError(error, 'Не удалось загрузить решение')
  }
};

export const handleUpdateTask = async (task_id, values, setTask) => {
  try {
    const taskData = {
      ...values,
      start_datetime: values.dateRange[0].toISOString(),
      end_datetime: values.dateRange[1].toISOString()
    };
    const updatedTask = await updateTask(task_id, taskData);
    setTask(updatedTask);
    return updatedTask;
  } catch (error) {
    fetchError(error, 'Не удалось обновить задание')
  }
};

export const handleDeleteTask = async (task_id, module_id, navigate) => {
  try {
    await deleteTask(task_id);
    navigate(`/modules/${module_id}`);
  } catch (error) {
    fetchError(error, 'Не удалось удалить задание')
  }
};