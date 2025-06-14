import axios from 'axios';

export const generateInviteLink = async (groupId, { expiresMinutes, isSingleUse }) => {
  const response = await axios.post(`/api/groups/${groupId}/invite/`, {
    expires_minutes: expiresMinutes,
    single_use: isSingleUse
  });
  return response.data;
};
