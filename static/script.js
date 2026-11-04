function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (message === "") return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user-msg">${message}</div>`;
    input.value = "";

    fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

document.addEventListener("DOMContentLoaded", function() {
    let btn = document.getElementById("send-btn");
    if (btn) {
        btn.addEventListener("click", sendMessage);
    }
    let input = document.getElementById("user-input");
    if (input) {
        input.addEventListener("keypress", function(e) {
            if (e.key === "Enter") sendMessage();
        });
    }
});
