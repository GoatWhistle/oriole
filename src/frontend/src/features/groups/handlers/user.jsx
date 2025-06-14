import { fetchError } from '../../api/error'

import { promoteUser, demoteUser, kickUser } from '../../groups/api/user';


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