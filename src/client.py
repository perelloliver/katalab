from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

google_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))