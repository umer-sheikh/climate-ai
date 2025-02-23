# agents/main_agent.py
import asyncio
from utils.image_processor import ImageProcessor
from config import Config
import requests
import json
from prompts import SYSTEM_PROMPT
from agents.search_agent import SearchAgent
from agents.llama_agent import LlamaAgent
from agents.rag_agent import RAGAgent
from agents.response_agent import ResponseAgent
from agents.base_agent import BaseAgent

class MainAgent(BaseAgent):
    def __init__(self):
        self.search_agent = SearchAgent()
        self.llama_agent = LlamaAgent()
        self.rag_agent = RAGAgent()
        self.response_agent = ResponseAgent()
        self.image_processor = ImageProcessor()
        self.api_key = Config.TOGETHER_API_KEY

    async def process_image_predictions(self, predictions, user_query=""):
        """Process image predictions through LLaMA for natural language description"""
        prompt = f"""As the MBZUAI Climate AI Assistant, user has given me satellite image for building damage analysis.

        Predictions is as follows:
        {json.dumps(predictions, indent=2)}

        User Query for the image:
        {user_query}

        Answer User Query using the prediction without mentioning file name. Response:"""

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 500,
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
            return response.json()['choices'][0]['message']['content'].strip()
        return json.dumps(predictions, indent=2)

    async def check_tool_requirement(self, query):
        """Determine if external tools (search/RAG) are needed"""
        prompt = f"""As an AI assistant, analyze if this query requires external tools to answer accurately.
        Common cases requiring tools:
        - Current weather, climate data, or environmental conditions
        - Recent events or news about climate initiatives
        - Specific statistics or data about UAE climate projects
        - Complex technical details that need verification
        
        Query: {query}
        
        Respond with a only JSON object containing:
        - needs_search: boolean (true if current/real-time data needed)
        - needs_rag: boolean (true if detailed UAE-specific knowledge needed)
        - explanation: string (brief reason for the decision)
        JSON: """

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 200,
            'temperature': 0.3,
            'messages': [
                {"role": "system", "content": "You are a tool selection expert."},
                {"role": "user", "content": prompt}
            ]
        }

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                'https://api.together.xyz/v1/chat/completions',
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Remove any type of code block formatting
                if content.startswith('```'):
                    # Split by newline and remove first and last lines (``` markers)
                    lines = content.split('\n')
                    content = '\n'.join(lines[1:-1])
                try:
                    result = json.loads(content.strip())
                    return result
                except json.JSONDecodeError:
                    print(f"Error parsing JSON: {content}")
                    # Fallback to using all tools
                    return {
                        "needs_search": True,
                        "needs_rag": True,
                        "explanation": "Failed to parse tool requirements, using all tools as fallback"
                    }
            return {"needs_search": True, "needs_rag": True, "explanation": "Failed to analyze, using all tools as fallback"}
        except Exception as e:
            print(f"Error in tool analysis: {e}")
            return {"needs_search": True, "needs_rag": True, "explanation": "Error in analysis, using all tools as fallback"}

    async def analyze_user_intent(self, chat_messages):
        """Analyze the full conversation to understand user's intent"""
        messages_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in chat_messages if msg['role'] in ['user', 'assistant']
        ])

        prompt = f"""Analyze this conversation and determine the user's current intent or question, 
        especially considering the context of previous messages. If the latest message is brief or 
        refers to previous context, incorporate that context in the intent.

        Conversation:
        {messages_text}

        Provide a clear, detailed statement of what the user is asking about or trying to understand
        User Message:"""

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 300,
            'temperature': 0.3,
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
            return response.json()['choices'][0]['message']['content'].strip()
        return chat_messages[-1]['content'] 
    
    async def process(self, chat_messages, base64_image=None):
        # If image is provided, process only image
        if base64_image:
            image_results = await self.image_processor.process_image(base64_image)
            if image_results:
                predictions_text = await self.process_image_predictions(image_results['predictions'], user_query=chat_messages[-1]['content'])
                return {
                    'message': predictions_text,
                    'annotated_image': f"data:image/jpeg;base64,{image_results['annotated_image']}"
                }
            return {
                'message': "Assistant: Sorry, I couldn't process the image properly.",
                'annotated_image': None
            }

        # For text queries, first check if we need external tools
        user_intent = await self.analyze_user_intent(chat_messages)
        # print(f"User Intent: {user_intent}")
        tool_requirements = await self.check_tool_requirement(user_intent)

        print(f"Tool Requirements: {tool_requirements}")
        
        tasks = []
        
        # Add necessary tools based on analysis
        if tool_requirements['needs_search']:
            tasks.append(self.search_agent.process(chat_messages))
        if tool_requirements['needs_rag']:
            tasks.append(self.rag_agent.process(chat_messages))
        if not tool_requirements['needs_search']:
            tasks.append(self.llama_agent.process(user_intent))
        
        # Run required tasks in parallel
        results = await asyncio.gather(*tasks)
        
        # Combine results based on which tools were used
        if len(results) == 1:
            # Only LLaMA was used
            final_response = results[0]
        else:
            # Multiple tools were used, combine results
            combined_response = await self.combine_results(*results)
            final_response = await self.response_agent.rephrase_response(combined_response)

        return {
            'message': final_response,
            'annotated_image': None
        }

    async def combine_results(self, llama_result, *tool_results):
        """Combine LLaMA result with any tool results"""
        if not tool_results:
            return llama_result

        results_text = f"""LLaMA Analysis:
        {llama_result}

        Additional Information:
        {' '.join(tool_results)}"""

        prompt = """Synthesize this information into a comprehensive response, 
        resolving any contradictions and providing a clear, accurate answer."""

        payload = {
            'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens': 1000,
            'temperature': 0.7,
            'messages': [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{prompt}\n\n{results_text}"}
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
            return response.json()['choices'][0]['message']['content'].strip()
        return results_text