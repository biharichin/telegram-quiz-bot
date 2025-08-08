import json
import os
import telegram
from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)

# Load questions
with open('mcqs.json', 'r') as f:
    questions = json.load(f)

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not bot_token:
    print("Error: Please set the TELEGRAM_BOT_TOKEN environment variable.")
else:
    bot = telegram.Bot(token=bot_token)

@app.route(f'/{bot_token}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        msg_id = update.message.message_id
        text = update.message.text.upper()

        if text == '/START':
            bot.sendMessage(chat_id=chat_id, text='Hello! I will send you questions daily. You can answer them by sending the option (e.g., A, B, C, D).', reply_to_message_id=msg_id)
        else:
            # Simplified answer checking
            for question in questions:
                if text == question['answer']:
                    bot.sendMessage(chat_id=chat_id, text=f"Correct! The answer to Q{question['id']} is indeed {question['answer']}.")
                    return 'ok'
            
            bot.sendMessage(chat_id=chat_id, text="I couldn't find a matching question for your answer. Please try again.", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    # The URL for your render app will be your Render service URL
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        return "Error: RENDER_EXTERNAL_URL not set."

    webhook_url = f'{render_url}/{bot_token}'
    s = bot.set_webhook(webhook_url)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # The port is set by Render, so we read it from the environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)