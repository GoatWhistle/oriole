import { useState, useEffect, useRef, useCallback } from "react";

export function useWebSocket({ groupId, userId }) {
  const [status, setStatus] = useState("Подключение...");
  const [messages, setMessages] = useState([]);
  const [myAccountId, setMyAccountId] = useState(null);

  const socketRef = useRef(null);

  useEffect(() => {
    if (!groupId || !userId) {
      setStatus("❌ Ошибка: отсутствуют groupId или userId");
      return;
    }

    const wsUrl = `ws://127.0.0.1:8000/api/websocket/?group_id=${groupId}&user_id=${userId}`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      setStatus(`🟢 Подключено как userId=${userId} в группе ${groupId}`);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "init") {
          setMyAccountId(data.account_id);
          return;
        }

        if (data.type === "history") {
          setMessages(data.messages);
          return;
        }

        if (data.edit) {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.message_id === data.message_id
                ? { ...msg, message: data.new_text || data.message }
                : msg
            )
          );
          return;
        }

        if (data.delete) {
          setMessages((prev) =>
            prev.filter((msg) => msg.message_id !== data.message_id)
          );
          return;
        }

        // Новое сообщение
        setMessages((prev) => [...prev, data]);
      } catch {
        console.warn("Невозможно обработать сообщение", event.data);
      }
    };

    socket.onclose = () => setStatus("🔴 Соединение закрыто");
    socket.onerror = () => setStatus("⚠️ Ошибка соединения");

    return () => {
      socket.close();
    };
  }, [groupId, userId]);

  // Функция отправки нового сообщения
  const sendMessage = useCallback(
    ({ message, replyToId = null, replyToText = null }) => {
      if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
        console.warn("WebSocket не подключен");
        return;
      }
      if (!message.trim()) return;

      const payload = {
        user_id: userId,
        group_id: groupId,
        message: message.trim(),
        reply_to: replyToId,
        reply_to_text: replyToText,
      };
      socketRef.current.send(JSON.stringify(payload));
    },
    [groupId, userId]
  );

  // Функция редактирования сообщения
  const editMessage = useCallback(
    (messageId, newText) => {
      if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;
      socketRef.current.send(
        JSON.stringify({
          edit: true,
          message_id: messageId,
          message: newText,
        })
      );
    },
    []
  );

  // Функция удаления сообщения
  const deleteMessage = useCallback(
    (messageId) => {
      if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;
      socketRef.current.send(
        JSON.stringify({
          delete: true,
          message_id: messageId,
        })
      );
    },
    []
  );

  return {
    status,
    messages,
    myAccountId,
    sendMessage,
    editMessage,
    deleteMessage,
  };
}
