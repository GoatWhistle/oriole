import React, { useState, useEffect } from "react";

function MessageInput({ initialText = "", onSend, replyTo, onCancelEdit }) {
  const [text, setText] = useState(initialText);

  useEffect(() => {
    setText(initialText);
  }, [initialText]);

  function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;

    onSend(text.trim());
    setText("");
  }

  return (
    <div style={{ padding: "8px", borderTop: "1px solid #ccc", background: "#f9f9f9" }}>
      {initialText && (
        <div className="reply-preview">
          <div className="reply-header">
            <strong>Редактирование сообщения</strong>
            <span className="cancel-reply" onClick={() => {
              setText("");
              onCancelEdit();
            }}>×</span>
          </div>
          <div className="reply-text">{initialText}</div>
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
        <input
          type="text"
          placeholder={replyTo ? `Ответ пользователю ${replyTo.account_id}` : "Введите сообщение..."}
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{
            flexGrow: 1,
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            fontSize: "16px"
          }}
        />
        <button type="submit" style={{ padding: "10px 16px" }}>
          {initialText ? "Обновить" : "Отправить"}
        </button>
      </form>
    </div>
  );
}

export default MessageInput;
