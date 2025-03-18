// TODO: clear cookies

import {postRequest, getRequest} from './utils.js';

let sessions = new Map();
let anySessionLoaded = false;

document.addEventListener("DOMContentLoaded", () => {
    clearCookies();
    loadSessions();
    document.querySelector(".new-session").addEventListener("click", newSession);;
    document.querySelector(".send-message").addEventListener("click", sendMessage);
});


async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const userInputValue = userInput.value
    if (!userInputValue) return;

    if (!anySessionLoaded)
        await createSession();

    const userMessage = document.createElement("div");
    userMessage.textContent = userInputValue;

    userInput.value = "";
    document.getElementsByClassName("send-message").disabled = true;
    appendMessage("user", userInputValue);
    document.getElementById('loading').classList.add('active');
    setTimeout(() => {
        postRequest("chat/", {"message": userInputValue}, (response) => {
            console.log(response);
            // We add user input here because we want to sure about backend process
            appendMessage("Assistant", response.message);
            document.getElementsByClassName("send-message").disabled = false;
            document.getElementById('loading').classList.remove('active');
    }), 2000
    })
}


async function createSession() {
    return new Promise((resolve, reject) => {
        getRequest("create-session/", (response) => {
            if (response.error) {
                alert(response.error);
                reject(response.error);
            } else {
                createSessionButton(response, undefined);
                anySessionLoaded = true;
                resolve(response);
            }
        })
    });
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


function loadChatHistory(sessionButton) {
    const sessionId = sessions.get(sessionButton)
    getRequest(`/session/${sessionId}`, (data) => {
        clearMessages();
        data.session_messages.forEach(msg => {
            console.log(msg)
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
            createSessionButton(sessionData, sessionListDiv);
        });
        if (anySessionLoaded)
            loadChatHistory();
    });
}


function createSessionButton(sessionData, sessionListDiv) {
    if (sessionListDiv == undefined)
        sessionListDiv = document.getElementById("sessions-name");
    const sessionLink = document.createElement("button");
    sessionLink.className = "session";
    const divSession = document.createElement("div");
    divSession.innerHTML = `${sessionData.session_name}`;
    sessionLink.appendChild(divSession);
    sessionLink.onclick = () => { loadChatHistory(sessionLink); };
    sessions.set(sessionLink, sessionData.session_id);
    sessionListDiv.appendChild(sessionLink);
    // TODO: Sort by updated date
}


function clearCookies() {
    anySessionLoaded = false;
    document.cookie = "session_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
}


function newSession() {
    anySessionLoaded = false;
    clearCookies()
    clearMessages();
}