import openai
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔐 Suas chaves reais
TELEGRAM_TOKEN = '7666054835:AAHEHyKwVAOwQjWYjQbbv9i7DDK6K4OL5pA'
OPENAI_API_KEY = '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'
URL = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/"

openai.api_key = "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"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(URL + "sendMessage", data=data)


def get_chatgpt_response(user_message):
    prompt = (f"Você é um conselheiro cristão chamado RespondeCristaoBot. "
              f"Responda com base bíblica, conforto, sabedoria e versículos. "
              f"A pergunta é: '{user_message}'")
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                                "role": "user",
                                                "content": prompt
                                            }],
                                            temperature=0.7,
                                            max_tokens=300)
    return response.choices[0].message["content"].strip()


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
