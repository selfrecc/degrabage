// Меня заебало жрать и обновлять 4 сайта. Это не жизнь, это говно.


// Show debug info on the page
function log(message) {
    const debugDiv = document.createElement('div');
    debugDiv.textContent = message;
    document.body.appendChild(debugDiv);
}

// Initialize
log('Script loaded');
Telegram.WebApp.ready();
Telegram.WebApp.expand();
log('Telegram WebApp initialized');

document.getElementById('ticketForm').addEventListener('submit', function(e) {
    e.preventDefault();
    log('Form submitted');

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    log('Data: ' + JSON.stringify(data));

    try {
        Telegram.WebApp.sendData(JSON.stringify(data));
        log('Data sent to bot');
    } catch (error) {
        log('Error: ' + error.message);
    }
});

// Show Telegram WebApp version
log('Version: ' + Telegram.WebApp.version);

