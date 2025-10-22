const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const userMessageInput = document.getElementById("userMessage");
const logoutBtn = document.getElementById("logoutBtn");

// ✅ Verificar JWT
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "index.html";
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ✅ Mensaje inicial
addMessage("¡Hola! Soy tu asistente Connect. ¿En qué puedo ayudarte hoy?", "bot");

// ✅ Enviar mensaje al backend
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = userMessageInput.value.trim();
  if (!message) return;

  // Mostrar mensaje del usuario
  addMessage(message, "user");
  userMessageInput.value = "";

  try {
    // Enviar al backend como ReporteRequest { query: "..." }
    const res = await fetch("http://localhost:8080/api/reportes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ query: message }),
    });

    if (res.status === 401) {
      addMessage("❌ Sesión expirada. Por favor inicia sesión nuevamente.", "bot");
      setTimeout(() => {
        localStorage.removeItem("token");
        window.location.href = "index.html";
      }, 2000);
      return;
    }

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || "Error en el servidor");
    }

    // ✅ Mostrar respuesta del backend
    const data = await res.text();
    addMessage(data, "bot");

  } catch (error) {
    console.error("Error:", error);
    addMessage("❌ No se pudo conectar con el servidor.", "bot");
  }
});

// ✅ Cerrar sesión
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "index.html";
});
