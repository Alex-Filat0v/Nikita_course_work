// Подключение к WebSocket
const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
    console.log("WebSocket connected");
};

socket.onmessage = (event) => {
    console.log("Message from server:", event.data);
};

// Пример функции для регистрации пользователя
async function registerUser(username, password, email) {
    const response = await fetch("http://localhost:8000/api/users/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username,
            password,
            email,
        }),
    });
    return await response.json();
}

// Пример функции для получения туров
async function getTours() {
    const response = await fetch("http://localhost:8000/api/tours/");
    return await response.json();
}