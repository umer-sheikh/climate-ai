from agents.base_agent import BaseAgent
from utils.rag_setup import collection
from utils.query_composer import QueryComposer

class RAGAgent(BaseAgent):
    def __init__(self):
        self.collection = collection
        self.query_composer = QueryComposer()
    
    async def process(self, chat_messages):
        search_query = await self.query_composer.compose_search_query(chat_messages)
        
        results = self.collection.query(
            query_texts=[search_query],
            n_results=1
        )
        
        if results and results['documents'] and results['documents'][0]:
            return results['documents'][0][0]
        return "No relevant information found in the knowledge base."