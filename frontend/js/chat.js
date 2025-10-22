const chatBox = document.getElementById("chatBox");
const chatForm = document.getElementById("chatForm");
const userMessageInput = document.getElementById("userMessage");
const logoutBtn = document.getElementById("logoutBtn");

// ✅ Verificar JWT
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "index.html";
}

// ✅ Función para agregar mensajes al chat
function addMessage(text, sender, status = "default") {
  const msg = document.createElement("div");
  msg.classList.add("message", sender, status);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ✅ Mensaje inicial
setTimeout(() => {
  addMessage("Hola, soy tu asistente Connect. ¿En qué puedo ayudarte hoy?", "bot");
}, 300);

// ✅ Enviar mensaje al backend
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = userMessageInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userMessageInput.value = "";

  try {
    const res = await fetch("http://localhost:8080/api/reportes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ query: message }),
    });

    // 🔹 Sesión expirada
    if (res.status === 401) {
      addMessage("Tu sesión ha expirado. Por favor, inicia sesión nuevamente.", "bot", "error");
      setTimeout(() => {
        localStorage.removeItem("token");
        window.location.href = "index.html";
      }, 2000);
      return;
    }

    // 🔹 Procesar respuesta
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.message || "Error en el servidor");
    }

    // 🔹 Mostrar mensaje según el estado devuelto
    switch (data.status) {
      case "success":
        addMessage(data.message, "bot", "success");
        if (data.data) addMessage(JSON.stringify(data.data, null, 2), "bot", "data");
        break;
      case "warning":
        addMessage(data.message, "bot", "warning");
        break;
      case "error":
        addMessage(data.message, "bot", "error");
        break;
      case "info":
        addMessage(data.message, "bot", "info");
        break;
      default:
        addMessage(data.message || "No se pudo interpretar la respuesta del servidor.", "bot");
        break;
    }

  } catch (error) {
    console.error("Error:", error);
    addMessage("No se pudo conectar con el servidor. Inténtalo más tarde.", "bot", "error");
  }
});

// ✅ Cerrar sesión
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "index.html";
});
