
document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://localhost:8000');

    // Авторизация
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('log-username').value;
            const password = document.getElementById('log-password').value;
            const msg = {
                action: "login",
                username,
                password
            };
            socket.send(JSON.stringify(msg));
        });
    }

    // Регистрация
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('reg-username').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            const msg = {
                action: "register",
                username,
                email,
                password
            };
            socket.send(JSON.stringify(msg));
        });
    }

    // Обработка ответа от сервера
    socket.addEventListener("message", (event) => {
        const res = JSON.parse(event.data);
        alert(res.message);
        if (res.status === "success" && res.user_id) {
            localStorage.setItem("user_id", res.user_id);
            window.location.href = "index.html";
        }
    });

    socket.addEventListener("open", () => console.log("WebSocket connected"));
    socket.addEventListener("close", () => console.log("WebSocket disconnected"));
    socket.addEventListener("error", (err) => console.error("WebSocket error:", err));
});
