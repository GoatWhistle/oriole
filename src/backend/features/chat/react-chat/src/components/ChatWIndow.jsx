import React, { useRef, useState, useEffect } from "react";
import Message from "./Message";
import ContextMenu from "./ContextMenu";

function ChatWindow({ messages, myAccountId, onReply, onEdit, onDelete }) {
  const messagesEndRef = useRef(null);
  const menuRef = useRef(null);

  const [contextMenuData, setContextMenuData] = useState(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    function handleClickOutside() {
      if (contextMenuData) setContextMenuData(null);
    }
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, [contextMenuData]);

  useEffect(() => {
    if (contextMenuData && menuRef.current) {
      const { innerWidth, innerHeight } = window;
      const menuRect = menuRef.current.getBoundingClientRect();

      let x = contextMenuData.x;
      let y = contextMenuData.y;

      if (x + menuRect.width > innerWidth) {
        x = innerWidth - menuRect.width - 10;
      }
      if (y + menuRect.height > innerHeight) {
        y = innerHeight - menuRect.height - 10;
      }
      if (x < 10) x = 10;
      if (y < 10) y = 10;

      if (x !== contextMenuData.x || y !== contextMenuData.y) {
        setContextMenuData(prev => ({ ...prev, x, y }));
      }
    }
  }, [contextMenuData]);

  const handleContextMenu = (e, message, isOwnMessage) => {
    e.preventDefault();

    setContextMenuData({ x: e.clientX, y: e.clientY, message, isOwn: isOwnMessage });
  };

  return (
    <div className="chat-window" style={{ position: "relative", height: "400px", overflowY: "auto" }}>
      {messages.map((msg) => (
        <Message
          key={msg.message_id}
          message={msg}
          isOwnMessage={String(msg.account_id) === String(myAccountId)}
          onContextMenu={(e) => handleContextMenu(e, msg, String(msg.account_id) === String(myAccountId))}
        />
      ))}
      <div ref={messagesEndRef} />
      {contextMenuData && (
        <ContextMenu
          ref={menuRef}
          x={contextMenuData.x}
          y={contextMenuData.y}
          isOwnMessage={contextMenuData.isOwn}
          onReply={() => {
            onReply(contextMenuData.message);
            setContextMenuData(null);
          }}
          onEdit={() => {
            onEdit(contextMenuData.message);
            setContextMenuData(null);
          }}
          onDelete={() => {
            if (window.confirm("Удалить сообщение?")) {
              onDelete(contextMenuData.message);
            }
            setContextMenuData(null);
          }}
          onClose={() => setContextMenuData(null)}
        />
      )}
    </div>
  );
}

export default ChatWindow;
