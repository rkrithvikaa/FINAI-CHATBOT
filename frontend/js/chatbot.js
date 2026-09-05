// ========================================
// FINAI - AI CHATBOT
// ========================================

const CHATBOT_API = "http://127.0.0.1:5000/api/chat";


// Send message
async function sendMessage() {

    const input = document.getElementById("chatInput");
    const message = input?.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    addMessage("Thinking...", "bot");

    try {

        const token = getToken();

        const response = await fetch(
            `${CHATBOT_API}/message`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );

        const data = await response.json();

        removeThinkingMessage();

        if (response.ok) {

            addMessage(
                data.response || data.message,
                "bot"
            );

        } else {

            addMessage(
                data.message || "Sorry, I couldn't understand that.",
                "bot"
            );
        }

    } catch (error) {

        console.error(error);

        removeThinkingMessage();

        addMessage(
            "Unable to connect to AI server.",
            "bot"
        );
    }
}


// Add message to chat
function addMessage(message, sender) {

    const chatBox = document.getElementById("chatBox");

    if (!chatBox) return;

    const messageDiv = document.createElement("div");

    messageDiv.className = `message ${sender}`;

    messageDiv.innerHTML = `
        <div class="message-content">
            ${escapeHTML(message)}
        </div>
    `;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Remove thinking
function removeThinkingMessage() {

    const messages =
        document.querySelectorAll(".message.bot");

    if (messages.length === 0) return;

    const lastMessage =
        messages[messages.length - 1];

    if (
        lastMessage.textContent.trim() === "Thinking..."
    ) {
        lastMessage.remove();
    }
}


// Prevent HTML injection
function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Enter key
document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("chatInput");

    if (input) {

        input.addEventListener("keydown", (event) => {

            if (event.key === "Enter") {
                sendMessage();
            }

        });
    }

});