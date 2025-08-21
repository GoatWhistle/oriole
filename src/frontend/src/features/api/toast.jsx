import { ExclamationCircleOutlined, CheckCircleOutlined, InfoCircleOutlined } from '@ant-design/icons';

export const fetchToast = (type = 'info', title, description) => {
  const getIcon = () => {
    switch (type) {
      case 'error':
        return <ExclamationCircleOutlined className="toast-icon" />;
      case 'success':
        return <CheckCircleOutlined className="toast-icon" />;
      case 'info':
        return <InfoCircleOutlined className="toast-icon" />;
      default:
        return null;
    }
  };

  return {
    type,
    title,
    description,
    getIcon
  };
};
