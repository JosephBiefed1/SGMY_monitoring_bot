# KTMB Service Bot

A data‐aggregation tool for monitoring travel conditions between Singapore and Malaysia checkpoints.It gathers:

- Weather forecasts from the Singapore Government API
- Human‐traffic sentiment from Telegram channel messages
- Train ticket availability from the KTMB booking site
- Motor‐vehicle traffic levels via YOLO image classification of checkpoint cameras
- Collates all data into combined CSVs for analysis or dashboarding

---

## Features

- **Weather** (`get_weather_forecast_information.py`)
- **Human Traffic** (`telegram_extract.py`, `telegram_bot.py`, `classification_model.py`)
- **Train Data** (`ktmb.py`)
- **Motor Traffic Images** (`motor_traffic.py`)
- **Motor Traffic Details** (`motor_details.py`)
- **Orchestration** (`combine_all.py`, `manager.py`)

---

## Requirements

- Python 3.8+
- Virtual environment

```sh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Environment Variables

Create a file named `.env` at the project root with these entries:

```dotenv
//USE TELETHON API TO EXTRACT THE TELEGRAM MESSAGES
TELEGRAM_BOT_ID_TOKEN=<your-telegram-bot-token>
API_ID=<your-api-id>
API_HASH=<your-api-hash>
PHONE_NUMBER=<your-phone-number>
SESSION_STRING=<your-telegram-session-string>
```

Example:

```dotenv
TELEGRAM_BOT_ID_TOKEN=744441333:A024325354nknfwffe
API_ID=20941343
API_HASH=032j4f303932nnfs
PHONE_NUMBER=+6599992222
SESSION_STRING=123venvjvjw9j3e3obfiufjd1jboi3ep32keebionmd
```

---

## How to Run

1. Load environment variables at the top of each script (e.g. in `telegram_bot.py`):

   ````python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # reads .env

   BOT_TOKEN      = os.getenv("TELEGRAM_BOT_ID_TOKEN")
   API_ID         = os.getenv("API_ID")
   API_HASH       = os.getenv("API_HASH")
   PHONE_NUMBER   = os.getenv("PHONE_NUMBER")
   SESSION_STRING = os.getenv("SESSION_STRING")
   ````
2. Run telegram bot modules below:

   ```powershell
   python telegram_bot.py
   ```
3. Outputs will be written into the `combined_data/` directory

---

## Project Structure

```
classification_model.py
combine_all.py
get_weather_forecast_information.py
ktmb.py
manager.py
motor_details.py
motor_traffic.py
telegram_bot.py
telegram_extract.py
combined_data/
motor_traffic_data/
ktmb_data/
human_traffic_data/
```

---
