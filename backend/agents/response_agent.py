from agents.base_agent import BaseAgent
from config import Config
import requests
from prompts import SYSTEM_PROMPT

class ResponseAgent(BaseAgent):
    def __init__(self):
        self.api_key = Config.TOGETHER_API_KEY

    async def rephrase_response(self, combined_results):
        prompt = f"""As the MBZUAI Climate AI Assistant, rephrase and structure the following 
        information into a clear, coherent response about UAE climate topics:

        {combined_results}

        Provide a well-organized response that maintains accuracy while being engaging and easy to understand."""

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 1000,
            'temperature': 0.7,
            'messages': [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
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

        if response.status_code == 200:
            return "Assistant: " + response.json()['choices'][0]['message']['content'].strip()
        return combined_results