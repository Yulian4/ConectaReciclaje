const registerForm = document.getElementById("registerForm");
const msg = document.getElementById("message");

registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    nombreCompleto: document.getElementById("nombreCompleto").value,
    tipoDoc: document.getElementById("tipoDoc").value,
    numeroDoc: document.getElementById("numeroDoc").value,
    telefono: document.getElementById("telefono").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    rol: document.getElementById("rol").value,
    idDireccion: parseInt(document.getElementById("idDireccion").value),
  };

  try {
    const res = await fetch("http://localhost:8080/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error("Error al registrar usuario");
    const result = await res.json();

    msg.textContent = "Registro exitoso. Ahora puedes iniciar sesión.";
    setTimeout(() => (window.location.href = "index.html"), 1500);
  } catch (err) {
    msg.textContent = err.message;
  }
});
