const socket = io.connect('http://127.0.0.1:5000'); // assuming you have initialized the socket connection

// assuming you have a div with id "message-container"
const messageContainer = document.getElementById("message-container");

// assuming you have a Python list of messages called "messages"
socket.on("moderation_queue", (moderation_queue) => 
{
    console.log("Received moderation_queue event with data: ", moderation_queue);
    messageContainer.innerHTML = moderation_queue.map(message => `<div>${message}</div>`).join("");
});
document.getElementById("moderation-form").addEventListener("submit", function(event){
    event.preventDefault();
  
    let action = event.submitter.name;
    fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        [action]: 'true'
      })
    }).then(response => {
      console.log(response);
    }).catch(error => {
      console.error(error);
    });
  });