
import os
from dotenv import load_dotenv

load_dotenv()    #loads the values from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")    #retrieves the API key