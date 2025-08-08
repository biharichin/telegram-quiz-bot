
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load questions
with open('mcqs.json', 'r') as f:
    questions = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I will send you questions daily. You can answer them by sending the option (e.g., A, B, C, D).')

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_answer = update.message.text.upper()
    user_id = update.message.from_user.id

    # This is a simplified logic. A more robust solution would be to store the last question sent to each user.
    # For now, we'll just check the answer against the entire list of questions.
    
    for question in questions:
        if user_answer == question['answer']:
            await update.message.reply_text(f"Correct! The answer to Q{question['id']} is indeed {question['answer']}.")
            return

    await update.message.reply_text("I couldn't find a matching question for your answer. Please try again.")

def main() -> None:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("Error: Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    application.run_polling()

if __name__ == '__main__':
    main()
