function sendMessage() {
    let input = document.getElementById("chatbot-input").value;
    let responseBox = document.getElementById("chatbot-response");

    if (input.trim() === "") return;

    responseBox.innerHTML += `<p><strong>You:</strong> ${input}</p>`;
    document.getElementById("chatbot-input").value = "";

    fetch("/chatbot", {
        method: "POST",
        body: new URLSearchParams({ message: input }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        let formattedReply = formatChatbotResponse(data.reply);
        responseBox.innerHTML += `<p><strong>AI:</strong> ${formattedReply}</p>`;
        responseBox.scrollTop = responseBox.scrollHeight;
    })
    .catch(() => responseBox.innerHTML += `<p><strong>AI:</strong> Sorry, an error occurred.</p>`);
}

function formatChatbotResponse(response) {
    return response
        .replace(/\*/g, "<strong>")  // Bold formatting
        .replace(/-/g, "<br>• ")      // Bullet points
        .replace(/\n/g, "<br>");      // Line breaks
}


