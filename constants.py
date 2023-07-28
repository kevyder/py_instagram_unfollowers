import os
from dotenv import load_dotenv

load_dotenv()

# Instagram
INSTAGRAM_URL = "https://instagram.com"
IGUSERNAME = os.environ.get("IGUSERNAME")
IGPASSWORD = os.environ.get("IGPASSWORD")
IGACCOUNT = os.environ.get("IGACCOUNT")

# Redis
REDIS_URL = os.environ.get("REDIS_URL")
