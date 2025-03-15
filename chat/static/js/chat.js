// TODO: clear cookies

import {postRequest, getRequest} from './utils.js';

document.addEventListener("DOMContentLoaded", loadSessions);
document.addEventListener("DOMContentLoaded", () => {
    loadSessions();
    document.querySelector(".new-session").addEventListener("click", newSession);;
    document.querySelector(".send-message").addEventListener("click", sendMessage);
});


function sendMessage() {
    const userInput = document.getElementById("user-input");
    const userInputValue = userInput.value
    if (!userInputValue) return;

    const userMessage = document.createElement("div");
    userMessage.textContent = userInputValue;

    userInput.value = "";
    document.getElementsByClassName("send-message").disabled = true;
    appendMessage("user", userInputValue);
    document.getElementById('loading').classList.add('active');
    setTimeout(() => {
        postRequest("chat/", {"message": userInputValue}, (response) => {
            // We add user input here because we want to sure about backend process
            console.log(response)
            appendMessage("Assistance", response.message);
            if (!doesSessionSet()) document.cookie = `chat_session_id=${response.session_id}; path=/`;
            loadSessions();  // TODO: not optimize
            document.getElementsByClassName("send-message").disabled = false;
            document.getElementById('loading').classList.remove('active');
        }), 2000
    })
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const divMessage = document.createElement("div")
    if (sender.toLowerCase() == "user") {
        divMessage.className = "user-prompt"
        divMessage.innerHTML = "<strong>You:</strong>";
    } else if (sender.toLowerCase() == "assistant") {
        divMessage.className = "ai-response"
        divMessage.innerHTML = "<strong>AI:</strong>";
    }
    divMessage.innerHTML += `${text}`;
    chatBox.appendChild(divMessage)
    chatBox.scrollTop = chatBox.scrollHeight;
}


function clearMessages() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
}


function loadChatHistory() {
    getRequest("/chat/", (data) => {
        clearMessages();
        data.session_messages.forEach(msg => {
            appendMessage(msg.role, msg.content);
        });
    });
}


function loadSessions() {
    getRequest("/sessions/", (data) => {
        const sessionListDiv = document.getElementById("sessions-name");
        const sessionListData = data.sessions;
        sessionListDiv.innerHTML = "";
        sessionListData.forEach(sessionData => {
            const sessionLink = document.createElement("button");
            sessionLink.className = "session";
            const divSession = document.createElement("div");
            divSession.innerHTML = `${sessionData.session_name}`;
            sessionLink.appendChild(divSession);
            sessionLink.onclick = () => {
                loadSession(sessionData.session_id);
            }
            sessionListDiv.appendChild(sessionLink);
        });
        if (doesSessionSet())
            loadChatHistory();
    });
}

function doesSessionSet() {
    const cookies = `; ${document.cookie}`;
    const parts = cookies.split(`; chat_session_id=`);
    return (parts == 2 && parts.pop().split(';').shift())
}


function loadSession(session_id) {
    document.cookie = `chat_session_id=${session_id}; path=/`;
    loadChatHistory();
}


function newSession() {
    document.cookie = `chat_session_id=; path=/`;
    clearMessages();
}