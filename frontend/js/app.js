document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Basic validation
            if (!username || !password) {
                alert('Username and password are required');
                return;
            }

            // Connect to WebSocket
            const socket = new WebSocket('ws://localhost:8000');

            socket.onopen = () => {
                console.log('Connected to server');
                const message = {
                    action: 'register',
                    username: username,
                    password: password
                };
                socket.send(JSON.stringify(message));
            };

            socket.onmessage = (event) => {
                const response = JSON.parse(event.data);
                if (response.status === 'success') {
                    alert('Registration successful! You can now login');
                    window.location.href = 'login.html';
                } else {
                    alert('Error: ' + response.message);
                }
                socket.close();
            };

            socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                alert('Connection error. Please try again.');
                socket.close();
            };
        });
    }
});