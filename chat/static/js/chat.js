// TODO: clear cookies

document.addEventListener("DOMContentLoaded", loadSessions);

function sendMessage() {
    userInput = document.getElementById("user-input");
    userInputValue = userInput.value
    if (!userInputValue) return;

    userMessage = document.createElement("div");
    userMessage.textContent = userInputValue;

    userInput.value = "";

    console.log(userInputValue);

    fetch('chat/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        },
        body: JSON.stringify({"message": userInputValue})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.error) console.alert(data.error)
        else {
            // We add user input here because we want to sure about backend process
            appendMessage("user", userInputValue);
            appendMessage("Assistance", data.message);
            loadSessions();  // TODO: not optimize
        }
    })
}

function appendMessage(sender, text) {
    let chatBox = document.getElementById("chat-box");
    if (sender.toLowerCase() == "user") {
        chatBox.innerHTML += `<div><strong>You:</strong> ${text}</div>`;
    } else if (sender.toLowerCase() == "assistance") {
        chatBox.innerHTML += `<div><strong>AI:</strong> ${text}</div>`;
    }
    else {
        console.log(`Wrong sender ${sender}`);
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}


function clearMessages() {
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
}


function loadChatHistory() {
    fetch("/chat/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(`Error: ${data.error}`)
            return
        }
        clearMessages();
        console.log(data);
        data.session_messages.forEach(msg => {
            appendMessage(msg.role, msg.content);
        });
    })
}


function loadSessions() {
    fetch("/sessions/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        }
    })
    .then(response => response.json())
    .then(data => {
        sessionListDiv = document.getElementById("session-list");
        sessionListData = data.sessions;
        sessionListDiv.innerHTML = "";
        sessionListData.forEach(sessionData => {
            sessionLink = document.createElement("button");
            console.log(sessionData)
            sessionLink.innerHTML = `<div> ${sessionData.session_name} </div>`
            sessionLink.onclick = () => {
                loadSession(sessionData.session_id);
            }
            sessionListDiv.appendChild(sessionLink);
        });
        const cookies = `; ${document.cookie}`;
        const part = cookies.split(`; chat_session_id=`);
        if (part.length == 2) {
            loadChatHistory();
        }
    })
}

function loadSession(session_id) {
    console.log(session_id)
    document.cookie = `chat_session_id=${session_id}; path=/`;
    loadChatHistory();
}