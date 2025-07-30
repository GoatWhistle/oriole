import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { useWebSocket } from "../hooks/useWebSocket";
import ChatWindow from "../components/ChatWindow";
import MessageInput from "../components/MessageInput";
import ReplyPreview from "../components/ReplyPreview";
import "../styles/ChatPage.css";

function ChatPage() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const groupId = queryParams.get("group_id");
  const userId = queryParams.get("user_id");

  const {
    status,
    messages,
    myAccountId,
    sendMessage,
    editMessage,
    deleteMessage,
  } = useWebSocket({ groupId, userId });

  const [replyTo, setReplyTo] = useState(null);
  const [editMessageData, setEditMessageData] = useState(null);

  function handleSendMessage(text) {
    if (editMessageData) {
      editMessage(editMessageData.message_id, text);
      setEditMessageData(null);
    } else {
      sendMessage({
        message: text,
        replyToId: replyTo ? replyTo.message_id : null,
        replyToText: replyTo ? replyTo.message : null,
      });
    }
    setReplyTo(null);
  }

  function handleReply(message) {
    setReplyTo(message);
    setEditMessageData(null);
  }

  function handleEdit(message) {
    setEditMessageData(message);
    setReplyTo(null);
  }

  function handleDelete(message) {
    deleteMessage(message.message_id);
  }

  return (
    <div className="chat-page">
      <header>Oriole Chat — Группа {groupId} — Статус: {status}</header>

      <div className="chat-container">
        <ChatWindow
          messages={messages}
          myAccountId={myAccountId}
          onReply={handleReply}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />

        {replyTo && (
          <ReplyPreview replyTo={replyTo} onCancel={() => setReplyTo(null)} />
        )}

        <MessageInput
          key={editMessageData?.message_id || "new"}
          initialText={editMessageData?.message || ""}
          onSend={handleSendMessage}
          replyTo={replyTo}
          onCancelEdit={() => setEditMessageData(null)}
        />
      </div>
    </div>
  );
}

export default ChatPage;
