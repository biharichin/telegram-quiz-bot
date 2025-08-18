# Indian Economy MCQs Telegram Bot

## Project Description

This project is a Telegram bot that sends multiple-choice questions (MCQs) about the Indian economy to specified Telegram chats. The bot is designed to be automated, sending a new set of questions daily. It also keeps track of the questions sent to avoid repetition.

## Features

- **Daily MCQs:** Automatically sends a batch of 20 MCQs every day.
- **Progress Tracking:** Remembers the last question sent and continues from there.
- **Interactive Quiz:** Users can answer the questions, and the bot will provide feedback on whether the answer is correct.
- **Webhook Support:** Uses a web server to receive updates from Telegram, making the bot responsive.
- **Automated Deployment:** The project is set up to be easily deployed and automated using GitHub Actions.

## Technology Stack

- **Backend:** Python
- **Telegram Bot Library:** `python-telegram-bot`
- **Web Framework:** Flask
- **Data Storage:** JSON files for MCQs (`mcqs.json`) and progress tracking (`progress.json`).
- **Automation:** GitHub Actions

## Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── main.yml        # GitHub Actions workflow for sending daily questions
│       └── sender.yml      # GitHub Actions workflow for sending questions on push
├── .gitignore
├── bot.py                # The main bot script with the Flask web server
├── mcqs.json             # The database of multiple-choice questions
├── part1_indian_economy.txt # Source text for questions
├── part2 indian_economics.txt # Source text for questions
├── progress.json         # Tracks the last sent question
├── requirements.txt      # Python dependencies
├── send_daily_questions.py # Script to send the daily questions
└── TODO.md               # A to-do list for the project
```

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.9 or higher
    *   Git

2.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    You will need to create a `.env` file in the root of the project and add the following environment variables:
    ```
    TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
    MY_CHAT_ID="your-telegram-chat-id"
    FRIEND_CHAT_ID="your-friends-telegram-chat-id"
    ```
    *   `TELEGRAM_BOT_TOKEN`: Your Telegram bot token, which you can get from the BotFather on Telegram.
    *   `MY_CHAT_ID`: Your personal Telegram chat ID.
    *   `FRIEND_CHAT_ID`: The chat ID of a friend or another chat where you want to send the questions.

## How it Works

The project consists of two main Python scripts:

1.  **`bot.py`:** This script runs a Flask web server that listens for incoming messages from Telegram. It uses a webhook to receive updates, which is more efficient than polling. When a user sends a message to the bot, this script processes the message and sends a response.

2.  **`send_daily_questions.py`:** This script is responsible for sending the daily MCQs. It reads the `mcqs.json` file to get the questions and the `progress.json` file to determine which questions to send. It then sends a batch of 20 questions to the specified chat IDs.

### Automation with GitHub Actions

The project uses GitHub Actions to automate the process of sending daily questions. There are two workflow files in the `.github/workflows` directory:

-   **`main.yml`:** This workflow is triggered on a schedule (daily at 1:30 AM UTC). It checks out the repository, installs the dependencies, and then runs the `send_daily_questions.py` script. After sending the questions, it commits and pushes the updated `progress.json` file to the repository.

-   **`sender.yml`:** This workflow is triggered on every push to the `main` branch. It performs the same steps as the `main.yml` workflow, allowing you to manually trigger the sending of questions by pushing a change to the repository.

## Configuration

-   **Adding Questions:** To add new questions, you can edit the `mcqs.json` file. Each question should have the following format:
    ```json
    {
      "id": 1,
      "question": "What is the capital of India?",
      "options": {
        "A": "Mumbai",
        "B": "New Delhi",
        "C": "Kolkata",
        "D": "Chennai"
      },
      "answer": "B"
    }
    ```

-   **Changing the Schedule:** You can change the schedule for sending daily questions by editing the `cron` expression in the `main.yml` file.
