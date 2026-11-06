const $ = (id) => document.getElementById(id);
const messagesEl = $("messages");
const chatArea = $("chatArea");
const input = $("messageInput");
const welcome = $("welcome");
const typing = $("typing");
let sessionId = sessionStorage.getItem("shopease_session") || "";
let lastUserQuery = "";

function scrollToBottom(smooth = true) {
  requestAnimationFrame(() => {
    try {
      chatArea.scrollTo({
        top: chatArea.scrollHeight,
        behavior: smooth ? "smooth" : "auto"
      });
    } catch (_) {
      chatArea.scrollTop = chatArea.scrollHeight;
    }
  });
}

function addMessage(role, text, data = {}) {
  welcome.classList.add("hidden");
  const row = document.createElement("div");
  row.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "assistant" ? "S" : "Y";
  const body = document.createElement("div");
  body.className = "message-body";
  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "assistant" ? "ShopEase Assistant" : "You";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  body.append(meta, bubble);

  if (role === "assistant") {
    if (data.category) {
      const tags = document.createElement("div");
      tags.className = "answer-tools";
      const category = document.createElement("span");
      category.className = "tag";
      category.textContent = `Topic · ${data.category}`;
      tags.append(category);
      if (data.needs_human_help) {
        const help = document.createElement("span");
        help.className = "tag";
        help.textContent = "Human support available";
        tags.append(help);
      }
      body.append(tags);
    }
    if (data.sources?.length) {
      const sources = document.createElement("div");
      sources.className = "source-line";
      sources.textContent = `Based on: ${data.sources.join(", ")}`;
      body.append(sources);
    }
    if (data.products?.length) {
      const grid = document.createElement("div");
      grid.className = "product-grid";
      data.products.forEach((product) => {
        const card = document.createElement("div");
        card.className = "product-card";
        if (product.thumbnail) {
          const image = document.createElement("img");
          image.src = product.thumbnail;
          image.alt = product.title;
          image.loading = "lazy";
          image.onload = () => scrollToBottom(true);
          image.onerror = () => image.remove();
          card.append(image);
        }
        const details = document.createElement("div");
        const title = document.createElement("strong");
        title.textContent = product.title;
        const category = document.createElement("small");
        category.textContent = `${product.category} · ${product.stock > 0 ? `${product.stock} in demo stock` : "Out of demo stock"}`;
        const price = document.createElement("div");
        price.className = "product-price";
        price.textContent = `$${Number(product.price).toFixed(2)}`;
        details.append(title, category, price);
        card.append(details);
        grid.append(card);
      });
      body.append(grid);
    }
  }
  row.append(avatar, body);
  messagesEl.append(row);
  scrollToBottom();
}

async function sendMessage(text) {
  const query = text.trim();
  if (!query) return;
  lastUserQuery = query;
  addMessage("user", query);
  input.value = "";
  input.style.height = "auto";
  typing.classList.remove("hidden");
  scrollToBottom(true);
  $("sendBtn").disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query, session_id: sessionId || null})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The request could not be completed.");
    sessionId = data.session_id;
    sessionStorage.setItem("shopease_session", sessionId);
    addMessage("assistant", data.answer, data);
  } catch (error) {
    addMessage("assistant", `I couldn't complete that request. ${error.message} Please try again or request human support.`);
  } finally {
    typing.classList.add("hidden");
    $("sendBtn").disabled = false;
    input.focus();
    scrollToBottom();
  }
}

$("chatForm").addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 120)}px`;
});
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    $("chatForm").requestSubmit();
  }
});
document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.prompt));
});

function openSupport() {
  $("supportQuery").value = lastUserQuery;
  $("ticketResult").classList.add("hidden");
  $("supportForm").classList.remove("hidden");
  $("supportModal").classList.remove("hidden");
}
$("supportBtn").addEventListener("click", openSupport);
$("closeModal").addEventListener("click", () => $("supportModal").classList.add("hidden"));
$("supportModal").addEventListener("click", (event) => {
  if (event.target === $("supportModal")) $("supportModal").classList.add("hidden");
});
$("supportForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("submitSupport");
  button.disabled = true;
  button.textContent = "Submitting...";
  try {
    const response = await fetch("/support", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: $("customerName").value,
        email: $("customerEmail").value,
        query: $("supportQuery").value,
        session_id: sessionId
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not submit the request.");
    $("supportForm").classList.add("hidden");
    const result = $("ticketResult");
    result.textContent = `Your request has been recorded. Ticket ID: ${data.ticket_id}. Status: ${data.status}. This is a demonstration support queue, not a live agent service.`;
    result.classList.remove("hidden");
  } catch (error) {
    $("ticketResult").textContent = error.message;
    $("ticketResult").classList.remove("hidden");
  } finally {
    button.disabled = false;
    button.textContent = "Submit support request";
  }
});

$("newChatBtn").addEventListener("click", async () => {
  if (sessionId) {
    try { await fetch(`/sessions/${encodeURIComponent(sessionId)}`, {method: "DELETE"}); } catch (_) {}
  }
  sessionId = "";
  lastUserQuery = "";
  sessionStorage.removeItem("shopease_session");
  messagesEl.replaceChildren();
  welcome.classList.remove("hidden");
  input.focus();
});



async function restoreSession() {
  if (!sessionId) return;
  try {
    const response = await fetch(`/sessions/${encodeURIComponent(sessionId)}`);
    if (!response.ok) return;
    const data = await response.json();
    (data.messages || []).forEach((message) => {
      addMessage(message.role, message.content);
      if (message.role === "user") lastUserQuery = message.content;
    });
    scrollToBottom(false);
  } catch (_) {
    // A missing or expired in-memory session simply starts with an empty view.
  }
}
restoreSession();
