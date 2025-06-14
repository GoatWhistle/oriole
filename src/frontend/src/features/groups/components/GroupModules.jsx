import React from 'react';
import { List, Card, Tag, Typography, Row, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const { Text, Title } = Typography;

export const GroupModules = ({ modules = [], userRole, onCreate, onSelect }) => {
  return (
    <>
      <Row justify="space-between" align="middle" style={{ marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>Модули:</Title>
        {(userRole === 0 || userRole === 1) && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={onCreate}
          >
            Создать модуль
          </Button>
        )}
      </Row>

      <List
        dataSource={modules}
        renderItem={module => (
          <List.Item>
            <Card
              size="small"
              title={module.title}
              style={{ width: '100%', cursor: 'pointer' }}
              extra={
                <Tag color={module.is_contest ? 'purple' : 'transparent'}>
                  {module.is_contest ? 'Контест' : ''}
                </Tag>
              }
              hoverable
              onClick={() => onSelect(module.id)}
            >
              <Text>
                Выполнено: {module.user_completed_tasks_count || 0} из {module.tasks_count || 0} задач
              </Text>
            </Card>
          </List.Item>
        )}
        locale={{ emptyText: 'В этой группе пока нет модулей' }}
      />
    </>
  );
};
