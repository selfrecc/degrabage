// Меня заебало жрать и обновлять 4 сайта. Это не жизнь, это говно.


document.getElementById('ticketForm').onsubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    Telegram.WebApp.sendData(JSON.stringify(data));
    Telegram.WebApp.close();
};

