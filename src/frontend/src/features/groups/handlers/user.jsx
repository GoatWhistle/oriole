import { fetchError } from '../../api/error'

import { promoteUser, demoteUser, kickUser, loadGroups, showGroupList } from '../../groups/api/user';


export const handlePromoteUser = async (groupId, userId) => {
  try {
    await promoteUser(groupId, userId);
    return { userId, newRole: 1 };
  } catch (error) {
    return fetchError(error, 'Не удалось повысить пользователя');
  }
};

export const handleDemoteUser = async (groupId, userId) => {
  try {
    await demoteUser(groupId, userId);
    return { userId, newRole: 2 };
  } catch (error) {
    return fetchError(error, 'Не удалось понизить пользователя');
  }
};

export const handleKickUser = async (groupId, userId) => {
  try {
    await removeUserFromGroup(groupId, userId);
    return userId;
  } catch (error) {
    return fetchError(error, 'Не удалось удалить пользователя');
  }
};

export const handleShowGroupList = async (setUserGroups, setLoading) => {
  try {
    const data = await showGroupList();

    if (data.length === 0) {
      setUserGroups([{
        key: 'no-groups',
        label: 'У вас пока нет групп',
        disabled: true
      }]);
    } else {
      const menuItems = data.map(group => ({
        key: group.id,
        label: group.title,
        title: group.description
      }));
      setUserGroups(menuItems);
    }

    setLoading(false);
  } catch (error) {
      return fetchError(error, 'Не удалось загрузить список групп пользователя');
  }
};