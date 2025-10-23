const form = document.getElementById("loginForm");
const messageDiv = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  try {
    const res = await fetch("http://localhost:8080/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error("Credenciales inválidas");
    const result = await res.json();

    localStorage.setItem("token", result.token);

    messageDiv.textContent = "Inicio de sesión exitoso, redirigiendo...";
    setTimeout(() => (window.location.href = "chat.html"), 1000);
  } catch (err) {
    messageDiv.textContent = err.message;
  }
});
