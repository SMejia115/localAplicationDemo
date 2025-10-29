const apiUrl = "http://127.0.0.1:5000";

document.getElementById("check-status").addEventListener("click", async () => {
  const res = await fetch(`${apiUrl}/status`);
  const data = await res.json();
  document.getElementById("server-status").innerText = data.status;
});

document.getElementById("send-btn").addEventListener("click", async () => {
  const message = document.getElementById("message-input").value;
  const res = await fetch(`${apiUrl}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  document.getElementById("response").innerText = data.response;
});

document.getElementById("fib-btn").addEventListener("click", async () => {
  const n = document.getElementById("fib-input").value;
  if (!n || n <= 0) {
    document.getElementById("fib-result").innerText = "Por favor, ingresa un número válido.";
    return;
  }

  const res = await fetch(`${apiUrl}/fibonacci/${n}`);
  if (res.ok) {
    const data = await res.json();
    document.getElementById("fib-result").innerText = data.fibonacci.join(", ");
  } else {
    document.getElementById("fib-result").innerText = "Error al generar la serie.";
  }
});
