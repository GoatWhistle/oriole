import { fetchError } from '../../api/error'
import { fetchUserRole } from '../../api/user_role'

import { createGroup,
        fetchGroup,
        leaveGroup,
        updateGroup,
        deleteGroup
} from '../../groups/api/group';

export const handleCreateGroup = async (values, setConfirmLoading, form, setOpen) => {
  setConfirmLoading(true);
  try {
    const groupData = {
      title: values.title,
      description: values.description || '',
    };

    const createdGroup = await createGroup(groupData);
    form.resetFields();
    setOpen(false);
    return createdGroup;
  } catch (error) {
    return fetchError(error, 'Ошибка при создании группы');
  } finally {
    setConfirmLoading(false);
    window.location.reload();
  }
};

export const handleFetchGroup = async (groupId) => {
  try {
    const [groupData, roleData] = await Promise.all([
      fetchGroup(groupId),
      fetchUserRole(groupId)
    ]);
    return { group: groupData, userRole: roleData };
  } catch (error) {
    return fetchError(error, 'Ошибка при получении данных о группе');
  }
};

export const handleLeaveGroup = async (groupId) => {
  try {
    await leaveGroup(groupId);
    return true;
  } catch (error) {
    return fetchError(error, 'Не удалось выйти из группы');
  }
};

export const handleUpdateGroup = async (groupId, values) => {
  try {
    const updatedGroup = await updateGroup(groupId, values);
    return updatedGroup;
  } catch (error) {
    return fetchError(error, 'Не удалось обновить группу');
  }
};

export const handleDeleteGroup = async (groupId) => {
  try {
    await deleteGroup(groupId);
    return true;
  } catch (error) {
    return fetchError(error, 'Не удалось удалить группу');
  }
};
