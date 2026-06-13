from pymongo import MongoClient
from app.core.config import *

client = MongoClient(MONGO_URI)

db = client[MONGO_DB]