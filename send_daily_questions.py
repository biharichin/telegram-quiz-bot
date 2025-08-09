
import asyncio
import json
import os
import telegram

async def send_questions():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids = [os.environ.get("MY_CHAT_ID"), os.environ.get("FRIEND_CHAT_ID")]
    
    if not bot_token or not all(chat_ids):
        print("Error: Please set the TELEGRAM_BOT_TOKEN, MY_CHAT_ID, and FRIEND_CHAT_ID environment variables.")
        return

    bot = telegram.Bot(token=bot_token)
    
    with open("mcqs.json", "r") as f:
        questions = json.load(f)
        
    with open("progress.json", "r+") as f:
        progress = json.load(f)
        last_sent_id = progress.get("last_sent_id", 0)
        print(f"[DEBUG] Initial last_sent_id: {last_sent_id}")
        
        start_index = last_sent_id
        end_index = start_index + 20
        
        if start_index >= len(questions):
            print("[DEBUG] No more questions to send.")
            for chat_id in chat_ids:
                await bot.send_message(chat_id=chat_id, text="No more questions, we are done!")
            return
            
        questions_to_send = questions[start_index:end_index]
        print(f"[DEBUG] Sending questions from index {start_index} to {end_index}.")
        print(f"[DEBUG] Questions to send: {[q['id'] for q in questions_to_send]}")
        
        for chat_id in chat_ids:
            for q in questions_to_send:
                question_text = f"Q{q['id']}: {q['question']}\n"
                options = [value for key, value in q['options'].items()]
                correct_option_id = ord(q['answer']) - ord('A')

                await bot.send_poll(
                    chat_id=chat_id,
                    question=question_text,
                    options=options,
                    type='quiz',
                    correct_option_id=correct_option_id
                )

        progress["last_sent_id"] = end_index
        print(f"[DEBUG] Updated last_sent_id to: {end_index}")
        f.seek(0)
        json.dump(progress, f, indent=4)

if __name__ == "__main__":
    asyncio.run(send_questions())
