import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Typography, Divider, Progress, List, Tag, Button, Space, Popconfirm, Spin } from 'antd';
import dayjs from 'dayjs';
import { handleGetModule, handleDeleteModule } from '../../handlers/module.jsx';
import CreateTaskModal from '../modals/CreateTaskModal/CreateTaskModal.jsx';
import EditModuleModal from '../modals/EditModuleModal/EditModuleModal.jsx';
import styles from './ModuleDetails.module.css';

const { Title, Text, Paragraph } = Typography;

const ModuleDetails = () => {
  const { module_id } = useParams();
  const navigate = useNavigate();
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [isCreateModalVisible, setIsCreateModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);

  useEffect(() => {
    const fetchModuleData = async () => {
      try {
        const role = await handleGetModule(module_id, setModule, setLoading);
        setUserRole(role);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchModuleData();
  }, [module_id]);

  const handleModuleUpdate = (updatedModule) => {
    setModule(updatedModule);
  };

  const completionPercentage = module?.tasks_count > 0
    ? Math.round((module.user_completed_tasks_count / module.tasks_count) * 100)
    : 0;

  const isAdmin = userRole === 0 || userRole === 1;

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" tip="Загрузка модуля..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <Card className={styles.errorCard}>
          <Title level={4} className={styles.errorTitle}>Ошибка загрузки модуля</Title>
          <Text className={styles.errorText}>{error}</Text>
          <Button
            type="primary"
            onClick={() => window.location.reload()}
            className={styles.retryButton}
          >
            Попробовать снова
          </Button>
        </Card>
      </div>
    );
  }

  if (!module) {
    return (
      <div className={styles.notFoundContainer}>
        <Card className={styles.notFoundCard}>
          <Title level={4}>Модуль не найден</Title>
          <Text>Запрошенный модуль не существует или был удален</Text>
          <Button
            type="primary"
            onClick={() => navigate('/')}
            className={styles.homeButton}
          >
            На главную
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card
        title={
          <div className={styles.header}>
            <Title level={2} className={styles.moduleTitle}>{module.title}</Title>
            {isAdmin && (
              <Space className={styles.actions}>
                <Button
                  type="primary"
                  onClick={() => setIsCreateModalVisible(true)}
                  className={styles.createButton}
                >
                  Создать задание
                </Button>
                <Button
                  type="default"
                  onClick={() => setIsEditModalVisible(true)}
                  className={styles.editButton}
                >
                  Редактировать модуль
                </Button>
                <Popconfirm
                  title="Вы уверены, что хотите удалить этот модуль?"
                  onConfirm={() => handleDeleteModule(module_id, navigate)}
                  okText="Да"
                  cancelText="Нет"
                  placement="topRight"
                >
                  <Button danger className={styles.deleteButton}>
                    Удалить модуль
                  </Button>
                </Popconfirm>
              </Space>
            )}
          </div>
        }
        className={styles.card}
      >
        <Paragraph className={styles.description}>{module.description}</Paragraph>

        <div className={styles.tagsContainer}>
          <Tag color={module.is_active ? 'green' : 'red'} className={styles.statusTag}>
            {module.is_active ? 'Активно' : 'Неактивно'}
          </Tag>
          {module.is_contest && (
            <Tag color="orange" className={styles.contestTag}>
              Контест
            </Tag>
          )}
        </div>

        <Divider className={styles.divider} />

        <div className={styles.datesContainer}>
          <Text strong className={styles.datesTitle}>Сроки выполнения:</Text>
          <div className={styles.dateItem}>
            <Text strong>Начало:</Text>
            <Text>{dayjs(module.start_datetime).format('DD.MM.YYYY HH:mm')}</Text>
          </div>
          <div className={styles.dateItem}>
            <Text strong>Окончание:</Text>
            <Text>{dayjs(module.end_datetime).format('DD.MM.YYYY HH:mm')}</Text>
          </div>
        </div>

        <Divider className={styles.divider} />

        <div className={styles.progressContainer}>
          <Text strong className={styles.progressTitle}>Прогресс выполнения:</Text>
          <Progress
            percent={completionPercentage}
            status={completionPercentage === 100 ? 'success' : 'active'}
            className={styles.progressBar}
            strokeColor={completionPercentage === 100 ? '#52c41a' : '#1890ff'}
          />
          <Text className={styles.progressText}>
            {module.user_completed_tasks_count} из {module.tasks_count} заданий выполнено
          </Text>
        </div>

        <Divider className={styles.divider} />

        <Title level={4} className={styles.tasksTitle}>Задачи:</Title>
        {module.tasks?.length > 0 ? (
          <List
            dataSource={module.tasks}
            renderItem={task => (
              <List.Item className={styles.taskItem}>
                <Card
                  size="small"
                  title={task.title}
                  className={styles.taskCard}
                  extra={
                    <Space className={styles.taskTags}>
                      {task.is_correct !== undefined && (
                        task.is_correct ? (
                          <Tag color="success" className={styles.completedTag}>Выполнено</Tag>
                        ) : (
                          <Tag color="warning" className={styles.notCompletedTag}>Не выполнено</Tag>
                        )
                      )}
                      <Tag
                        color={task.is_active ? 'green' : 'red'}
                        className={styles.taskStatusTag}
                      >
                        {task.is_active ? 'Активна' : 'Неактивна'}
                      </Tag>
                    </Space>
                  }
                >
                  <Paragraph className={styles.taskDescription}>{task.description}</Paragraph>
                  <Button
                    type="primary"
                    onClick={() => navigate(`/tasks/${task.id}`)}
                    className={styles.taskButton}
                  >
                    Перейти к задаче
                  </Button>
                </Card>
              </List.Item>
            )}
            className={styles.tasksList}
          />
        ) : (
          <Card className={styles.noTasksCard}>
            <Text>В этом модуле пока нет заданий</Text>
          </Card>
        )}
      </Card>

      <CreateTaskModal
        visible={isCreateModalVisible}
        onCancel={() => setIsCreateModalVisible(false)}
        moduleId={module_id}
        module={module}
        onTaskCreated={handleModuleUpdate}
        navigate={navigate}
      />

      <EditModuleModal
        visible={isEditModalVisible}
        onCancel={() => setIsEditModalVisible(false)}
        module={module}
        onModuleUpdated={handleModuleUpdate}
      />
    </div>
  );
};

export default ModuleDetails;
