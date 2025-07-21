from flask import Flask, request
import openai
import os

from openai import OpenAI

app = Flask(__name__)

# Configure corretamente as chaves
TELEGRAM_TOKEN = '7666054835:AAHEHyKwVAOwQjWYjQbbv9i7DDK6K4OL5pA'
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def send_message(chat_id, text):
    import requests
    data = {"chat_id": chat_id, "text": text}
    requests.post(URL + "sendMessage", data=data)

def get_chatgpt_response(user_message):
    prompt = (
        f"Você é um conselheiro cristão chamado RespondeCristaoBot. "
        f"Responda com base bíblica, conforto, sabedoria e versículos. "
        f"A pergunta é: '{user_message}'"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"].get("text", "")
        reply = get_chatgpt_response(message_text)
        send_message(chat_id, reply)
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
