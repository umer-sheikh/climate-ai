from agents.base_agent import BaseAgent
from config import Config
from utils.query_composer import QueryComposer
import requests
import json

class SearchAgent(BaseAgent):
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.query_composer = QueryComposer()

    async def process(self, chat_messages):
        search_query = await self.query_composer.compose_search_query(chat_messages)
        
        payload = {
            "api_key": self.api_key,
            "query": search_query,
            "search_depth": "basic",
            "include_answer": True,
            "max_results": 5
        }
        
        response = requests.post('https://api.tavily.com/search', json=payload)
        return response.json().get('answer')