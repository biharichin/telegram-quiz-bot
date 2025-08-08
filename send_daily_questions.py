
import json
import os
import telegram

def send_questions():
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
        
        start_index = last_sent_id
        end_index = start_index + 20
        
        if start_index >= len(questions):
            for chat_id in chat_ids:
                bot.send_message(chat_id=chat_id, text="No more questions, we are done!")
            return
            
        questions_to_send = questions[start_index:end_index]
        
        for chat_id in chat_ids:
            for q in questions_to_send:
                question_text = f"Q{q['id']}: {q['question']}\n"
                options = ""
                for key, value in q['options'].items():
                    options += f"{key}: {value}\n"
                
                bot.send_message(chat_id=chat_id, text=question_text + options)

        progress["last_sent_id"] = end_index
        f.seek(0)
        json.dump(progress, f, indent=4)

if __name__ == "__main__":
    send_questions()
