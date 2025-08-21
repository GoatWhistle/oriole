import { Button, Popconfirm, Space, Typography } from 'antd';
import { EditOutlined, CloseOutlined, LogoutOutlined, PlusOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

export const GroupHeader = ({ group, userRole, onEdit, onInvite, onDelete, onLeave }) => (
  <>
    <Title level={2}>{group.title}</Title>
    <Paragraph>{group.description}</Paragraph>
    <Space style={{ marginBottom: '16px' }}>
      {(userRole === 0 || userRole === 1) && (
        <Button type="primary" onClick={onInvite} icon={<PlusOutlined />}>
          Пригласить участников
        </Button>
      )}
      {userRole === 0 && (
        <>
          <Button icon={<EditOutlined />} onClick={onEdit}>
            Редактировать группу
          </Button>
          <Popconfirm
            title={`Вы уверены, что хотите удалить группу "${group.title}"?`}
            onConfirm={onDelete}
            okText="Да, удалить"
            cancelText="Отмена"
            okButtonProps={{ danger: true }}
          >
            <Button danger icon={<CloseOutlined />}>
              Удалить группу
            </Button>
          </Popconfirm>
        </>
      )}
      <Popconfirm
        title={`Вы уверены, что хотите покинуть группу "${group.title}"?`}
        onConfirm={onLeave}
        okText="Да"
        cancelText="Нет"
      >
        <Button danger icon={<LogoutOutlined />}>
          Покинуть группу
        </Button>
      </Popconfirm>
    </Space>
  </>
);
