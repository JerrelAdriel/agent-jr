const API_URL = "/api";
let messages = [];
let isLoading = false;

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 160) + "px";
}

function scrollToBottom() {
  const container = document.getElementById("chatContainer");
  container.scrollTop = container.scrollHeight;
}

function removeWelcome() {
  const welcome = document.querySelector(".welcome");
  if (welcome) welcome.remove();
}

function createMessage(role, content) {
  const div = document.createElement("div");
  div.className = `message ${role}`;

  if (role === "ai") {
    div.innerHTML = `
      <div class="msg-avatar">JR</div>
      <div class="msg-bubble">${content}</div>
    `;
  } else {
    div.innerHTML = `<div class="msg-bubble">${escapeHtml(content)}</div>`;
  }

  return div;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}

function renderMarkdown(text) {
  return text
    .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    .replace(/^- (.+)$/gm, "<li>$1</li>")
    .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>");
}

async function sendMessage() {
  if (isLoading) return;

  const input = document.getElementById("inputBox");
  const text = input.value.trim();
  if (!text) return;

  removeWelcome();
  isLoading = true;
  document.getElementById("sendBtn").disabled = true;

  input.value = "";
  input.style.height = "auto";

  messages.push({ role: "user", content: text });

  const container = document.getElementById("chatContainer");
  container.appendChild(createMessage("user", text));

  // Typing indicator
  const typingEl = document.createElement("div");
  typingEl.className = "message ai typing";
  typingEl.innerHTML = `
    <div class="msg-avatar">JR</div>
    <div class="msg-bubble">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  container.appendChild(typingEl);
  scrollToBottom();

  let fullReply = "";

  try {
    const res = await fetch(`${API_URL}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
    });

    typingEl.remove();

    const aiMsg = createMessage("ai", "");
    const bubble = aiMsg.querySelector(".msg-bubble");
    const cursor = document.createElement("span");
    cursor.className = "cursor";
    bubble.appendChild(cursor);
    container.appendChild(aiMsg);
    scrollToBottom();

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") break;
          try {
            const parsed = JSON.parse(data);
            fullReply += parsed.text;
            bubble.innerHTML = renderMarkdown(fullReply);
            const newCursor = document.createElement("span");
            newCursor.className = "cursor";
            bubble.appendChild(newCursor);
            scrollToBottom();
          } catch {}
        }
      }
    }

    bubble.innerHTML = renderMarkdown(fullReply);
    messages.push({ role: "assistant", content: fullReply });

  } catch (err) {
    typingEl.remove();
    const errMsg = createMessage("ai", "Maaf, terjadi kesalahan. Pastikan server sudah berjalan! 😅");
    container.appendChild(errMsg);
    scrollToBottom();
    messages.pop();
  }

  isLoading = false;
  document.getElementById("sendBtn").disabled = false;
  input.focus();
}

function clearChat() {
  messages = [];
  const container = document.getElementById("chatContainer");
  container.innerHTML = `
    <div class="welcome">
      <div class="welcome-avatar">J</div>
      <h2>Hei! Aku Agent-JR 👋</h2>
      <p>Asisten AI pribadi kamu. Tanya apa aja, aku siap bantu!</p>
    </div>
  `;
}

document.getElementById("inputBox").focus();
