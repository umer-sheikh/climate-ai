class BaseAgent:
    """Base class for all agents"""
    async def process(self, *args, **kwargs):
        """Process method to be implemented by all agents"""
        raise NotImplementedError