// Меня заебало жрать и обновлять 4 сайта. Это не жизнь, это говно.


Telegram.WebApp.ready();
Telegram.WebApp.expand();

document.getElementById('ticketForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    console.log('Sending data:', data);  // Debug log

    // Send data back to bot
    Telegram.WebApp.sendData(JSON.stringify(data));
});

