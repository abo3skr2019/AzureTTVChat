function updateMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            const messageContainer = document.getElementById('message-container');
            messageContainer.innerHTML = '';

            if (data.message) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.innerHTML = '<p>' + data.message + '</p>';
                messageContainer.appendChild(messageDiv);
            } else {
                const noMessageDiv = document.createElement('div');
                noMessageDiv.className = 'no-message';
                noMessageDiv.innerHTML = '<p>No messages for moderation.</p>';
                messageContainer.appendChild(noMessageDiv);
            }
        })
        .catch(error => console.error(error));
}

// Periodically update messages every 1 seconds (adjust as needed)
setInterval(updateMessages, 1000);