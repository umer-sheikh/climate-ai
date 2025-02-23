from langchain.prompts import PromptTemplate

SYSTEM_PROMPT = """I am MBZUAI Climate AI Assistant. Today's date is February 23, 2025. 
I am a specialized AI assistant focused on climate-related topics specific to the UAE context. 
I will provide detailed information about climate change impacts, sustainability initiatives, 
and environmental policies in the UAE. I will politely decline to engage with topics 
outside of UAE climate and environmental concerns."""

SEARCH_QUERY_TEMPLATE = PromptTemplate(
    input_variables=["chat_history", "user_message"],
    template="""Based on the following chat history and user message, 
    generate a search query focused on UAE climate and environmental topics:
    Chat History: {chat_history}
    User Message: {user_message}
    Search Query:"""
)

LLAMA_QUERY_TEMPLATE = PromptTemplate(
    input_variables=["user_message"],
    template="""Generate a detailed response about UAE climate context for:
    {user_message}"""
)

RAG_QUERY_TEMPLATE = PromptTemplate(
    input_variables=["user_message"],
    template="""Convert the following user question into a RAG query about UAE climate:
    {user_message}"""
)