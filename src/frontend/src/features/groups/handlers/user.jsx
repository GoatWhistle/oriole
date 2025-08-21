import { fetchError } from '../../api/error'

import { promoteUser, demoteUser, kickUser, loadGroups, showGroupList } from '../../groups/api/user';


export const handlePromoteUser = async (spaceId, userId) => {
  try {
    await promoteUser(spaceId, userId);
    return { userId, newRole: 1 };
  } catch (error) {
    return fetchError(error, 'Не удалось повысить пользователя');
  }
};

export const handleDemoteUser = async (spaceId, userId) => {
  try {
    await demoteUser(spaceId, userId);
    return { userId, newRole: 2 };
  } catch (error) {
    return fetchError(error, 'Не удалось понизить пользователя');
  }
};

export const handleKickUser = async (spaceId, userId) => {
  try {
    await removeUserFromGroup(spaceId, userId);
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
