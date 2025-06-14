import { fetchError } from '../../api/error';

import { generateInviteLink } from '../../groups/api/invite';

export const handleGenerateInvite = async (groupId, settings) => {
  try {
    const data = await generateInviteLink(groupId, settings);
    return data;
  } catch (error) {
    return fetchError(error, 'Ошибка при генерации ссылки');
  }
};

export const handleCopyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
};
