import { showUserProfile,
         updateUserProfile,
         resetPassword,
         logoutUser,
         deleteUserAccount
} from '../api/user.jsx';

import { fetchError } from '../../api/error'


export const handleShowUserProfile = async (setUser, setLoading) => {
  try {
    const userData = await showUserProfile();
    setUser(userData);
  } catch (error) {
    fetchError(error, 'Ошибка загрузки профиля');
  } finally {
    setLoading(false);
  }
};

export const handleUpdateProfile = async (values, setUser) => {
  try {
    const updatedData = {
      name: values.name,
      surname: values.surname,
      patronymic: values.patronymic,
    };
    const userData = await updateUserProfile(updatedData);
    setUser(userData);
    return true;
  } catch (error) {
    fetchError(error, 'Ошибка при обновлении профиля');
    return false;
  }
};

export const handleResetPassword = async (setResetLoading) => {
  try {
    setResetLoading(true);
    const response = await resetPassword();
    message.success(response.message || 'Ссылка для сброса пароля отправлена на ваш email');
  } catch (error) {
    fetchError(error, 'Не удалось отправить ссылку для сброса пароля');
  } finally {
    setResetLoading(false);
  }
};

export const handleLogout = async (navigate) => {
  try {
    await logoutUser();
    navigate('/login');
  } catch (error) {
    fetchError(error, 'Ошибка при выходе из системы');
  }
};

export const handleDeleteAccount = async (navigate) => {
  try {
    await deleteUserAccount();
    navigate('/login');
  } catch (error) {
    fetchError(error, 'Произошла ошибка при удалении аккаунта');
  }
};