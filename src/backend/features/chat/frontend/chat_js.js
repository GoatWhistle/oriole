const params = new URLSearchParams(window.location.search);
const groupId = params.get("group_id");
const userId = params.get("user_id");
if (!groupId || !userId) {
    alert("❌ Не указан group_id или user_id");
    throw new Error("group_id или user_id отсутствует");
}

const connectionId = crypto.randomUUID();
let socket;
let replyToId = null;
let replyToText = "";
window.myAccountId = null;
window.editingMessageId = null;

let contextMenuElem = null;
let contextMenuVisible = false;

const messagesContainer = document.getElementById("messages");
const scrollDownBtn = document.getElementById("scrollDownBtn");

function updateStatus(text) {
    document.getElementById("status").textContent = text;
}

function formatTimestamp(ts) {
    return ts ? new Date(ts).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}) : "";
}

function hideContextMenu() {
    if (contextMenuElem) {
        contextMenuElem.style.display = "none";
        contextMenuVisible = false;
        contextMenuElem = null;
    }
}

function showContextMenu(x, y, messageId, messageText, isOwnMessage) {
    hideContextMenu();

    contextMenuElem = document.createElement("div");
    contextMenuElem.className = "context-menu";

    const replyBtn = document.createElement("button");
    replyBtn.textContent = "Ответить";
    replyBtn.onclick = () => {
        replyToId = messageId;
        replyToText = messageText;
        document.getElementById("replyToText").textContent = replyToText;
        document.getElementById("replyPreview").style.display = "block";
        hideContextMenu();
        document.getElementById("input").focus();
    };
    contextMenuElem.appendChild(replyBtn);

    if (isOwnMessage) {
        const editBtn = document.createElement("button");
        editBtn.textContent = "Редактировать";
        editBtn.onclick = () => {
            startEditingMessage(messageId, messageText);
            hideContextMenu();
        };
        contextMenuElem.appendChild(editBtn);

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Удалить";
        deleteBtn.onclick = () => {
            if (confirm("Вы действительно хотите удалить это сообщение?")) {
                deleteMessage(messageId);
            }
            hideContextMenu();
        };
        contextMenuElem.appendChild(deleteBtn);
    }

    document.body.appendChild(contextMenuElem);

    const menuRect = contextMenuElem.getBoundingClientRect();
    const winWidth = window.innerWidth;
    const winHeight = window.innerHeight;

    if (x + menuRect.width > winWidth) {
        x = winWidth - menuRect.width - 5;
    }
    if (y + menuRect.height > winHeight) {
        y = winHeight - menuRect.height - 5;
    }

    contextMenuElem.style.left = `${x}px`;
    contextMenuElem.style.top = `${y}px`;
    contextMenuElem.style.display = "block";
    contextMenuVisible = true;
}

function addMessage(msg, cssClass) {
    if (document.getElementById("msg-" + msg.message_id)) return;

    const div = document.createElement("div");
    div.className = `message ${cssClass || (String(msg.account_id) === String(window.myAccountId) ? "sent" : "received")}`;
    div.id = "msg-" + msg.message_id;

    const uid = document.createElement("div");
    uid.className = "user-id";
    uid.textContent = msg.account_id;
    div.append(uid);

    if (msg.reply_to && msg.reply_to_text) {
        const rb = document.createElement("div");
        rb.className = "reply-to-block";
        rb.textContent = `ОТВЕТ ПОЛЬЗОВАТЕЛЮ ${msg.reply_to}:`;
        const rt = document.createElement("div");
        rt.textContent = msg.reply_to_text.length > 100
            ? msg.reply_to_text.slice(0, 97) + "..."
            : msg.reply_to_text;
        rb.append(rt);
        rb.onclick = e => {
            e.stopPropagation();
            const targetMsg = document.getElementById("msg-" + msg.reply_to);
            if (targetMsg) {
                targetMsg.scrollIntoView({behavior: "smooth", block: "center"});
                targetMsg.classList.add("highlighted");
                setTimeout(() => targetMsg.classList.remove("highlighted"), 1500);
            }
        };
        div.append(rb);
    }

    const textDiv = document.createElement("div");
    textDiv.textContent = msg.message;
    div.append(textDiv);

    const bottom = document.createElement("div");
    bottom.className = "bottom-row";
    const ts = document.createElement("div");
    ts.className = "timestamp";
    ts.textContent = formatTimestamp(msg.timestamp);
    bottom.append(ts);
    div.append(bottom);

    if (String(msg.account_id) === String(window.myAccountId)) {
        div.addEventListener("contextmenu", e => {
            e.preventDefault();
            showContextMenu(e.pageX, e.pageY, msg.message_id, msg.message, true);
        });
    }

    messagesContainer.append(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function cancelReply() {
    replyToId = null;
    replyToText = "";
    document.getElementById("replyPreview").style.display = "none";
}

function startEditingMessage(messageId, oldText) {
    const input = document.getElementById("input");
    input.value = oldText;
    input.focus();
    window.editingMessageId = messageId;
}

function deleteMessage(messageId) {
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({
        delete: true,
        message_id: messageId,
    }));
}

function sendMessage() {
    const input = document.getElementById("input");
    const text = input.value.trim();

    if (!text || !socket || socket.readyState !== WebSocket.OPEN) return;

    if (window.editingMessageId) {
        socket.send(JSON.stringify({
            edit: true,
            message_id: window.editingMessageId,
            message: text,
        }));
        window.editingMessageId = null;
    } else {
        socket.send(JSON.stringify({
            user_id: userId,
            connectionId,
            message: text,
            reply_to: replyToId,
            reply_to_text: replyToText
        }));
    }

    input.value = "";
    cancelReply();
}

function connect() {
    if (!groupId || !userId) {
        updateStatus("❌ Не указан group_id или user_id");
        return;
    }

    socket = new WebSocket(`ws://127.0.0.1:8000/api/websocket/?group_id=${groupId}&user_id=${userId}`);

    socket.onopen = () => {
        updateStatus(`🟢 Подключено как user_id=${userId} в группе ${groupId}`);
    };

    socket.onmessage = e => {
        let d;
        try {
            d = JSON.parse(e.data);
        } catch {
            return;
        }

        if (d.type === "init") {
            window.myAccountId = d.account_id;
            updateStatus(`🟢 Подключено как user_id=${userId} в группе ${groupId}, account_id=${window.myAccountId}`);
            return;
        }

        if (d.type === "history") {
            d.messages.forEach(msg => {
                const cssClass = String(msg.account_id) === String(window.myAccountId) ? "sent" : "received";
                addMessage(msg, cssClass);
            });
        } else if (d.edit) {
            const md = document.getElementById("msg-" + d.message_id);
            if (md) {
                const textDiv = md.querySelector("div:nth-last-child(2)");
                if (textDiv) textDiv.textContent = d.new_text || d.message || "";
            }
        } else if (d.delete) {
            const md = document.getElementById("msg-" + d.message_id);
            if (md) md.remove();
        } else {
            const cssClass = String(d.account_id) === String(window.myAccountId) ? "sent" : "received";
            addMessage(d, cssClass);
        }
    };

    socket.onclose = () => updateStatus("🔴 Соединение закрыто");
    socket.onerror = () => updateStatus("⚠️ Ошибка соединения");
}

function onMessagesScroll() {
    const scrollFromBottom = messagesContainer.scrollHeight - messagesContainer.clientHeight - messagesContainer.scrollTop;
    if (scrollFromBottom > 100) {
        scrollDownBtn.style.display = "block";
    } else {
        scrollDownBtn.style.display = "none";
    }
}

scrollDownBtn.onclick = () => {
    messagesContainer.scrollTo({top: messagesContainer.scrollHeight, behavior: "smooth"});
};

window.onload = function () {
    connect();

    document.getElementById("sendBtn").addEventListener("click", sendMessage);

    document.getElementById("input").addEventListener("keydown", e => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    messagesContainer.addEventListener("scroll", onMessagesScroll);

    document.addEventListener("click", () => {
        if (contextMenuVisible) hideContextMenu();
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && contextMenuVisible) hideContextMenu();
    });
};
