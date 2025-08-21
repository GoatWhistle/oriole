import { fetchError } from '../../api/error.jsx'
import { fetchCheckAuth } from '../../api/check_auth.jsx';
import { fetchUserRole } from '../../api/user_role.jsx';

import { createModule,
         getModule,
         createTask,
         deleteModule,
         updateModule
} from '../api/module.jsx';

export const handleCreateModule = async (groupId, values) => {
  try {
    const moduleData = {
      title: values.title,
      description: values.description || "",
      is_contest: values.is_contest || false,
      group_id: parseInt(groupId),
      start_datetime: values.dateRange[0].toISOString(),
      end_datetime: values.dateRange[1].toISOString()
    };

    const module = await createModule(moduleData);
    return module;
  } catch (error) {
    return fetchError(error, 'Не удалось создать модуль');
  }
};

export const handleGetModule = async (module_id, setModule, setLoading) => {
  try {
    setLoading(true);
    const moduleData = await getModule(module_id);
    const role = await fetchUserRole(moduleData.group_id);
    setModule(moduleData);
    setLoading(false);
    return role;
  } catch (err) {
    setLoading(false);
    fetchError(err, err.message);
    throw err;
  }
};

export const handleCreateTask = async (values, module_id, navigate, setModule) => {
  try {
    const taskData = {
      ...values,
      module_id: parseInt(module_id),
      start_datetime: values.dateRange[0].toISOString(),
      end_datetime: values.dateRange[1].toISOString()
    };
    const task = await createTask(taskData);
    const updatedData = await getModule(module_id);
    setModule(updatedData);
    navigate(`/tasks/${task.id}`);
    return true;
  } catch (err) {
    fetchError(err, err.message);
    return false;
  }
};

export const handleDeleteModule = async (module_id, navigate) => {
  try {
    await deleteModule(module_id);
    navigate('/');
    return true;
  } catch (err) {
    fetchError(err, err.message);
    return false;
  }
};

export const handleUpdateModule = async (module_id, values, setModule) => {
  try {
    const moduleData = {
      ...values,
      start_datetime: values.dateRange[0].toISOString(),
      end_datetime: values.dateRange[1].toISOString()
    };
    const updatedModule = await updateModule(module_id, moduleData);
    setModule(updatedModule);
    return true;
  } catch (err) {
    fetchError(err, err.message);
    return false;
  }
};
