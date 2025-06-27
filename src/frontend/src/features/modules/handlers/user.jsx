import { fetchError } from '../../api/error'

import { showModuleList } from '../../modules/api/user';

export const handleShowModuleList = async (setUserModules, setLoading) => {
  try {
    const data = await showModuleList();

    if (data.length === 0) {
      setUserModules([{
        key: 'no-modules',
        label: 'У вас пока нет модулей',
        disabled: true
      }]);
    } else {
      const menuItems = data.map(module => ({
        key: module.id,
        label: module.title,
        title: module.description
      }));
      setUserModules(menuItems);
    }

    setLoading(false);
  } catch (error) {
      return fetchError(error, 'Не удалось загрузить список модулей пользователя');
  }
};