from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
    TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
    ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY')