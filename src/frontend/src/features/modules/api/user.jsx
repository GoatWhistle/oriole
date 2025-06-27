export const showModuleList = async () => {
  const response = await fetch('/api/modules/');
  return await response.json();
};
