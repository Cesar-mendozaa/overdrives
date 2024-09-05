const socket = new WebSocket('ws://localhost:8080');

const sendBtn = document.getElementById('send-btn');
const chatInput = document.getElementById('chat-input');
const chatBody = document.getElementById('chat-body');

socket.addEventListener('open', (event) => {
    console.log('Conectado al servidor WebSocket');
});

socket.addEventListener('message', (event) => {
    const botMessage = document.createElement('div');
    botMessage.classList.add('message-bot');
    botMessage.innerHTML = `<p class="texto-bot">${event.data}</p>`;
    chatBody.appendChild(botMessage);
    chatBody.scrollTop = chatBody.scrollHeight;
});

sendBtn.addEventListener('click', () => {
    const message = chatInput.value;
    if (message.trim()) {
        socket.send(message);
        const userMessage = document.createElement('div');
        userMessage.classList.add('message-user');
        userMessage.innerHTML = `<p class="texto-user">${message}</p>`;
        chatBody.appendChild(userMessage);
        chatBody.scrollTop = chatBody.scrollHeight;

        chatInput.value = '';
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});
