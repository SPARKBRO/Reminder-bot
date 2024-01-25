import os
from datetime import datetime
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv(".env")

# Initialize the Telegram client
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

client = Client("your_session_name", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Connect to MongoDB
db_url = os.environ["DB_URL"]
cluster = MongoClient(db_url)
db = cluster["reminders"]
collection = db["reminders"]

# Function to add a reminder to the database
def add_reminder(user, chat, message, date, location):
    reminder = {"user": user, "chat": chat, "message": message, "date": date, "location": location}
    collection.insert_one(reminder)

# Function to handle the /start command
@client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    # Reply with the start message
    await message.reply_text("Hello there! I am an admin reminder bot that works in both group and private chats.")

# Function to handle the /remind command
@client.on_message(filters.command("remind"))
async def remind_command(client, message: Message):
    # Ask users for the reminder location preference
    await message.reply_text("Where would you like to set the reminder? Please specify 'group' or 'pm'.")

# Function to handle images
@client.on_message(filters.photo & (filters.private | filters.group))
async def handle_images(client, message: Message):
    # Process the received image, for example, download and save it
    # You can access the image file_id using message.photo.file_id

# Add more event handlers and functions for handling reminders, media, etc.

# Start the bot
client.run()
