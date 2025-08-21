import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Divider, Typography, Spin, message } from 'antd';

import { GroupHeader } from '../GroupHeader.jsx';
import { GroupMembers } from '../GroupMembers.jsx';
import { GroupModules } from '../GroupModules.jsx';

import { InviteSettingsModal } from '../modals/InviteSettingsModal.jsx';
import { InviteLinkModal } from '../modals/InviteLinkModal.jsx';
import { EditGroupModal } from '../modals/EditGroupModal.jsx';
import { CreateModuleModal } from '../modals/CreateModuleModal.jsx';


import {
    handleFetchGroup,
  handleLeaveGroup,
  handleUpdateGroup,
  handleDeleteGroup
} from '../../handlers/group.jsx';

import { handleGenerateInvite, handleCopyToClipboard } from '../../handlers/invite.jsx';
import {
    handlePromoteUser,
  handleDemoteUser,
  handleKickUser
} from '../../handlers/user.jsx';
import { handleCreateModule } from '../../../modules/handlers/module.jsx';


const { Title } = Typography;

const GroupDetails = () => {
  const { group_id } = useParams();
  const navigate = useNavigate();

  const [state, setState] = useState({
    group: null,
    userRole: null,
    loading: true,
    error: null,
    inviteLink: null,
    expiryTime: null,
    isInviteSettingsModalOpen: false,
    isInviteLinkModalOpen: false,
    isEditModalOpen: false,
    isCreateModuleModalOpen: false
  });

  useEffect(() => {
    const loadGroupData = async () => {
      try {
        const { group, userRole } = await handleFetchGroup(group_id);
        setState(prev => ({
          ...prev,
          group,
          userRole,
          loading: false
        }));
      } catch (error) {
        setState(prev => ({
          ...prev,
          error: error.message,
          loading: false
        }));
      }
    };

    loadGroupData();
  }, [group_id]);

  const updateState = (updates) => {
    setState(prev => ({ ...prev, ...updates }));
  };

  const generateInvite = async (settings) => {
      const { link, expiryTime } = await handleGenerateInvite(group_id, settings);
      updateState({
        inviteLink: link,
        expiryTime,
        isInviteSettingsModalOpen: false,
        isInviteLinkModalOpen: true
      });
  };

  const kickUser = async (userId) => {
      await handleRemoveUser(group_id, userId);
      updateState(prev => ({
        ...prev,
        group: {
          ...prev.group,
          accounts: prev.group.accounts.filter(account => account.user_id !== userId)
        }
      }));
  };

  const leaveGroup = async () => {
      await handleLeaveGroup(group_id);
      navigate('/');
  };

  const promoteUser = async (userId) => {
      await handlePromoteUser(group_id, userId);
      updateState(prev => ({
        ...prev,
        group: {
          ...prev.group,
          accounts: prev.group.accounts.map(account =>
            account.user_id === userId ? { ...account, role: 1 } : account
          )
        }
      }));
  };

  const demoteUser = async (userId) => {
      await handleDemoteUser(group_id, userId);
      updateState(prev => ({
        ...prev,
        group: {
          ...prev.group,
          accounts: prev.group.accounts.map(account =>
            account.user_id === userId ? { ...account, role: 2 } : account
          )
        }
      }));
  };

  const updateGroup = async (values) => {
      const updatedGroup = await handleUpdateGroup(group_id, values);
      updateState({
        group: updatedGroup,
        isEditModalOpen: false
      });
  };

  const deleteGroup = async () => {
      await handleDeleteGroup(group_id);
      navigate('/');
  };

const createModule = async (values) => {
      const newModule = await handleCreateModule(group_id, values);
      updateState(prev => ({
        ...prev,
        group: {
          ...prev.group,
          modules: [...prev.group.modules, newModule]
        },
        isCreateModuleModalOpen: false
      }));
      window.location.reload();
  };

  const moduleClick = (moduleId) => {
    navigate(`/modules/${moduleId}`);
  };

  const copyToClipboard = () => {
    handleCopyToClipboard(state.inviteLink);
  };

  if (state.loading) return (
      <div>
        <Spin size="large" tip="Загрузка модуля..." />
      </div>
    );

  if (state.error) return <div>Ошибка: {state.error}</div>;
  if (!state.group) return <div>Группа не найдена</div>;

  return (
    <div style={{ padding: '100px'}}>
      <Card>
        <GroupHeader
          group={state.group}
          userRole={state.userRole}
          onEdit={() => updateState({ isEditModalOpen: true })}
          onInvite={() => updateState({ isInviteSettingsModalOpen: true })}
          onDelete={deleteGroup}
          onLeave={leaveGroup}
        />

        <Divider />

        <Title level={4}>Участники:</Title>
        <GroupMembers
          accounts={state.group.accounts}
          userRole={state.userRole}
          onPromote={promoteUser}
          onDemote={demoteUser}
          onRemove={kickUser}
        />

        <Divider />

        <GroupModules
          modules={state.group.modules}
          userRole={state.userRole}
          onCreate={() => updateState({ isCreateModuleModalOpen: true })}
          onSelect={moduleClick}
        />
      </Card>

      <InviteSettingsModal
        visible={state.isInviteSettingsModalOpen}
        onCancel={() => updateState({ isInviteSettingsModalOpen: false })}
        onGenerate={generateInvite}
      />

      <InviteLinkModal
        visible={state.isInviteLinkModalOpen}
        inviteLink={state.inviteLink}
        expiryTime={state.expiryTime}
        onCancel={() => updateState({ isInviteLinkModalOpen: false })}
        onCopy={copyToClipboard}
      />

      <EditGroupModal
        visible={state.isEditModalOpen}
        group={state.group}
        onCancel={() => updateState({ isEditModalOpen: false })}
        onSave={updateGroup}
      />

      <CreateModuleModal
        visible={state.isCreateModuleModalOpen}
        onCancel={() => updateState({ isCreateModuleModalOpen: false })}
        onCreate={createModule}
      />
    </div>
  );
};
export default GroupDetails;
