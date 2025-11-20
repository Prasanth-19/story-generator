from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("STORY_DB_URI")

client = MongoClient(MONGO_URI)
db = client["storydb"]
collection = db["stories"]

def save_story(prompt, genre, story):
    collection.insert_one({
        "prompt": prompt,
        "genre": genre,
        "story": story,
        "timestamp": datetime.now()
    })

def get_all_stories():
    return list(collection.find().sort("timestamp", -1))
