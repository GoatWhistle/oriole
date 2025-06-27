import { fetchError } from '../../api/error'

import { createModule } from '../../modules/api/module';

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