from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="FastAPI vs Go API")

# --- Существующие эндпоинты ---
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/call-go")
def call_go():
    r = requests.get("http://localhost:8080/ping")
    return {"go_response": r.json()}

# --- HTML-страница для WebSocket чата, подключающаяся к Go ---
@app.get("/chat", response_class=HTMLResponse)
async def get_chat_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Чат через Go WebSocket</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            #messages { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #f9f9f9; }
            #message-input { width: 70%; padding: 10px; }
            #username-input { width: 20%; padding: 10px; margin-right: 5px; }
            #send-btn { padding: 10px 20px; }
            .message { margin: 5px 0; border-bottom: 1px solid #eee; }
            .username { font-weight: bold; color: #2c3e50; }
            .time { font-size: 0.8em; color: #7f8c8d; margin-left: 10px; }
        </style>
    </head>
    <body>
        <h1>WebSocket Чат (подключение к Go-серверу)</h1>
        <div id="messages"></div>
        <input type="text" id="username-input" placeholder="Ваше имя" value="User">
        <input type="text" id="message-input" placeholder="Введите сообщение...">
        <button id="send-btn">Отправить</button>

        <script>
            // Подключаемся к WebSocket серверу Go (порт 8080)
            const ws = new WebSocket("ws://localhost:8080/ws");
            const messagesDiv = document.getElementById("messages");
            const messageInput = document.getElementById("message-input");
            const usernameInput = document.getElementById("username-input");
            const sendBtn = document.getElementById("send-btn");

            // Получение сообщения от сервера
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const messageDiv = document.createElement("div");
                messageDiv.className = "message";
                const username = data.username || "Аноним";
                const text = data.text || data;
                const time = data.time || new Date().toLocaleTimeString();
                messageDiv.innerHTML = `<span class="username">${escapeHtml(username)}</span>: 
                                         <span>${escapeHtml(text)}</span>
                                         <span class="time">${time}</span>`;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            };

            // Отправка сообщения
            function sendMessage() {
                const text = messageInput.value.trim();
                if (text === "") return;
                const username = usernameInput.value.trim() || "Аноним";
                ws.send(JSON.stringify({
                    username: username,
                    text: text,
                    time: new Date().toLocaleTimeString()
                }));
                messageInput.value = "";
            }

            sendBtn.onclick = sendMessage;
            messageInput.onkeypress = function(e) {
                if (e.key === "Enter") sendMessage();
            };

            function escapeHtml(text) {
                const div = document.createElement("div");
                div.textContent = text;
                return div.innerHTML;
            }
        </script>
    </body>
    </html>
    """
    return html_content