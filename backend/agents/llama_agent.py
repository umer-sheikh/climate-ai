from agents.base_agent import BaseAgent
from config import Config
from utils.query_composer import QueryComposer
import requests
from prompts import SYSTEM_PROMPT

class LlamaAgent(BaseAgent):
    def __init__(self):
        self.api_key = Config.TOGETHER_API_KEY
        self.query_composer = QueryComposer()
        
    async def process(self, user_intent):
        search_query = await self.query_composer.compose_search_query(user_intent)
        
        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 512,
            'temperature': 0.7,
            'messages': [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": search_query}
            ]
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.together.xyz/v1/chat/completions',
            json=payload,
            headers=headers
        )
        return response.json()['choices'][0]['message']['content']