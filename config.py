import os
from dotenv import load_dotenv
load_dotenv()
class Setting:
    secret_key = os.getenv("SECRET_KEY")
    algorithm = "HS256"
    access_token_expires = 30
    refresh_token_expires = 60