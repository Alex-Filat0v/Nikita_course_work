const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    console.log("Server:", msg);
    alert(`[${msg.status}] ${msg.message || ''}`);
};

function send(action, data) {
    ws.send(JSON.stringify({ action, data }));
}

function setupForms() {
    const regForm = document.getElementById('register-form');
    if (regForm) {
        regForm.addEventListener('submit', e => {
            e.preventDefault();
            send('register', {
                username: regForm.username.value,
                password: regForm.password.value
            });
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', e => {
            e.preventDefault();
            send('login', {
                username: loginForm.username.value,
                password: loginForm.password.value
            });
        });
    }

    const subForm = document.getElementById('subscribe-form');
    if (subForm) {
        subForm.addEventListener('submit', e => {
            e.preventDefault();
            send('subscribe', { email: subForm.email.value });
        });
    }

    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', e => {
            e.preventDefault();
            send('update_profile', {
                username: profileForm.username.value,
                fullname: profileForm.fullname.value,
                birthdate: profileForm.birthdate.value,
                phone: profileForm.phone.value,
                bio: profileForm.bio.value
            });
        });
    }

    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', e => {
            e.preventDefault();
            send('search_tours', {
                country: searchForm.country.value,
                date: searchForm.date.value
            });
        });
    }

    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', e => {
            e.preventDefault();
            const participants = parseInt(bookingForm.participants.value);
            const passport_data = [];
            for (let i = 0; i < participants; i++) {
                passport_data.push(bookingForm[`passport${i+1}`].value);
            }
            send('book_tour', {
                username: bookingForm.username.value,
                tour_title: bookingForm.tour_title.value,
                date: bookingForm.date.value,
                participants,
                passport_data
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', setupForms);