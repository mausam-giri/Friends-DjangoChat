const friendUsername = document.getElementById("friend-username").value;

async function sendMessage() {
  const messageInput = document.getElementById("chat-message-input");
  // const friendUsername = document.getElementById("friend-username").value;
  console.log(messageInput, friendUsername);
  if (messageInput.value.trim()) {
    const response = await fetch("/chat-app/messages/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        action: "send",
        message: messageInput.value.trim(),
        friend: friendUsername,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      displayMessages([data.message], true);
      messageInput.value = "";
    }
  }
}

async function fetchMessages(friendUsername) {
  const response = await fetch("/chat-app/messages/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      action: "fetch",
      friend: friendUsername,
    }),
  });

  const data = await response.json();
  if (data.status === "success") {
    displayMessages(data.messages);
  } else {
    console.error(data.message);
  }
}

function displayMessages(messages, append = false) {
  const messageContainer = document.getElementById("message-container");

  console.log(messages);
  if (!messages || messages?.length == 0) {
    messageContainer.innerHTML = `
       <div class="h-full flex items-center justify-center w-full text-highlight font-medium">
          Say Hello!
        </div>
    `;
    return;
  }

  if (!append) {
    messageContainer.innerHTML = "";
  }

  messages.forEach((msg) => {
    // const messageElement = document.getElementById("message-element");
    // // messageElement.classList.add("message");
    // const messageText = document.getElementById("message-element-text");
    // const messageTime = document.getElementById("message-element-time");
    // messageElement.classList.add(
    //   msg.sender === friendUsername ? "message-sent" : "message-received"
    // );
    // messageText.innerText = msg.mesage;
    // messageTime.innerText = msg.created_at;

    const msgStyle =
      msg.sender === friendUsername ? "message-received" : "message-sent";
    const message = `
      <div class="rounded-lg my-1 p-2 text-sm flex flex-col relative ${msgStyle}" id="message-element">
        <p class="" id="message-element-text">${msg.message}</p>
        <p class="text-gray-500 text-xs text-right leading-none" id="message-element-time">${msg.created_at}</p>
    </div>
    `;

    messageContainer.innerHTML += message;
  });

  messageContainer.scrollTop = messageContainer.scrollHeight;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].split("=");
      if (cookie[0] === name) {
        cookieValue = decodeURIComponent(cookie[1]);
        break;
      }
    }
  }
  return cookieValue;
}
