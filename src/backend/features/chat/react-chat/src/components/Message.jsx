import React, { useRef } from "react";

function Message({ message, isOwnMessage, onReply, onEdit, onDelete, onContextMenu }) {
  const messageRef = useRef(null);

  return (
    <div
      className={`message ${isOwnMessage ? "sent" : "received"}`}
      id={`msg-${message.message_id}`}
      ref={messageRef}
      onContextMenu={(e) => onContextMenu(e, message, isOwnMessage)}
    >
      <div className="user-id">{message.account_id}</div>

      {message.reply_to && message.reply_to_text && (
        <div
          className="reply-to-block"
          onClick={() => {
            const el = document.getElementById(`msg-${message.reply_to}`);
            if (el) {
              el.scrollIntoView({ behavior: "smooth", block: "center" });
              el.classList.add("highlighted");
              setTimeout(() => el.classList.remove("highlighted"), 1500);
            }
          }}
        >
          ОТВЕТ ПОЛЬЗОВАТЕЛЮ {message.account_id}:
          <div>
            {message.reply_to_text.length > 100
              ? message.reply_to_text.slice(0, 97) + "..."
              : message.reply_to_text}
          </div>
        </div>
      )}

      <div>{message.message}</div>

      <div className="bottom-row">
        <div className="timestamp">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
          {message.is_edited && <span className="edited-mark"> (edited)</span>}
        </div>
      </div>
    </div>
  );
}

export default Message;
