import React from "react";

function ReplyPreview({ replyTo, onCancel }) {
  if (!replyTo) return null;

  return (
    <div
      style={{
        padding: "8px",
        backgroundColor: "#f0f0f0",
        borderLeft: "4px solid #007bff",
        margin: "8px 0",
        position: "relative",
      }}
    >
      <strong>Ответ пользователю {replyTo.account_id}:</strong>{" "}
      <span>
        {replyTo.message.length > 100
          ? replyTo.message.slice(0, 97) + "..."
          : replyTo.message}
      </span>

      <button
        onClick={onCancel}
        style={{
          position: "absolute",
          right: "8px",
          top: "8px",
          border: "none",
          background: "transparent",
          fontSize: "16px",
          cursor: "pointer",
        }}
        title="Отменить ответ"
      >
        ×
      </button>
    </div>
  );
}

export default ReplyPreview;
