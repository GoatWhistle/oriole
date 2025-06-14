import { List, Avatar, Tag, Button, Popconfirm } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, CloseOutlined } from '@ant-design/icons';

const getRoleName = (role) => {
  const roles = {
    0: 'Создатель',
    1: 'Учитель',
    2: 'Ученик'
  };
  return roles[role];
};

const getRoleColor = (role) => {
  const colors = {
    0: 'red',
    1: 'orange',
    2: 'green'
  };
  return colors[role];
};

export const GroupMembers = ({ accounts, userRole, onPromote, onDemote, onRemove }) => (
  <List
    dataSource={accounts}
    renderItem={account => (
      <List.Item
        actions={
          userRole === 0 ? [
            account.role === 2 ? (
              <Popconfirm
                title="Повысить этого пользователя до учителя?"
                onConfirm={() => onPromote(account.user_id)}
                okText="Да"
                cancelText="Нет"
              >
                <Button type="text" style={{ color: '#52c41a' }} icon={<ArrowUpOutlined />} size="small" />
              </Popconfirm>
            ) : account.role === 1 ? (
              <Popconfirm
                title="Понизить этого пользователя до ученика?"
                onConfirm={() => onDemote(account.user_id)}
                okText="Да"
                cancelText="Нет"
              >
                <Button type="text" danger icon={<ArrowDownOutlined />} size="small" />
              </Popconfirm>
            ) : null,
            account.role === 2 && (
              <Popconfirm
                title="Вы уверены, что хотите удалить этого пользователя из группы?"
                onConfirm={() => onRemove(account.user_id)}
                okText="Да"
                cancelText="Нет"
              >
                <Button type="text" danger icon={<CloseOutlined />} size="small" />
              </Popconfirm>
            )
          ] : []
        }
      >
        <List.Item.Meta
          avatar={<Avatar>{account.user_id}</Avatar>}
          title={`user${account.user_id}`}
          description={
            <Tag color={getRoleColor(account.role)}>
              {getRoleName(account.role)}
            </Tag>
          }
        />
      </List.Item>
    )}
  />
);