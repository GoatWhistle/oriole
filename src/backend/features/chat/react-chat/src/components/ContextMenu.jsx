import React, { useEffect, useRef } from "react";

const ContextMenu = React.forwardRef(({ x, y, isOwnMessage, onReply, onEdit, onDelete, onClose }, ref) => {
  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        onClose();
      }
    }
    function handleEsc(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEsc);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEsc);
    };
  }, [onClose, ref]);

  return (
    <div
      ref={ref}
      className="context-menu"
      style={{
        position: "fixed",
        top: y,
        left: x,
        background: "#fff",
        border: "1px solid #ccc",
        zIndex: 10000,
        boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
        minWidth: 150,
        borderRadius: 6,
      }}
      onClick={(e) => e.stopPropagation()}
    >
      <button onClick={onReply}>Ответить</button>
      {isOwnMessage && (
        <>
          <button onClick={onEdit}>Редактировать</button>
          <button onClick={onDelete}>Удалить</button>
        </>
      )}
    </div>
  );
});

export default ContextMenu;
