from config import Config
import requests
import json

class QueryComposer:
    def __init__(self):
        self.api_key = Config.TOGETHER_API_KEY

    async def compose_search_query(self, user_message):
        

        prompt = f"""Create a question to ask to LLM after analyzing the user intent. Only return question without any additional information.

        User Intent:
        {user_message}

        Question:"""

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 100,
            'temperature': 0.3,
            'messages': [
                {"role": "system", "content": "You are an expert to create question from user intent."},
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
            print(response.json()['choices'][0]['message']['content'].strip())
            return response.json()['choices'][0]['message']['content'].strip()
        return "No relevant information found in the knowledge base."