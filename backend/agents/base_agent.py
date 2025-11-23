"""
Base agent class for all LangGraph agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from app.core.config import settings
from app.core.logger import app_logger


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = ChatAnthropic(
            model=settings.CLAUDE_MODEL,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            max_tokens=settings.MAX_TOKENS,
            temperature=0.7
        )
        app_logger.info(f"Initialized agent: {name}")

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task

        Args:
            task: Dictionary containing task parameters

        Returns:
            Dictionary containing execution results
        """
        pass

    def create_prompt(self, context: Dict[str, Any]) -> str:
        """Create a prompt for the LLM based on context"""
        return f"""You are {self.name}, a specialized AI agent.
Description: {self.description}

Context: {context}

Please analyze the provided context and complete your assigned task."""

    async def invoke_llm(self, prompt: str) -> str:
        """Invoke the LLM with a prompt"""
        try:
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            app_logger.error(f"Error invoking LLM for {self.name}: {e}")
            return f"Error: {str(e)}"

    def format_response(self, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format agent response"""
        return {
            "agent": self.name,
            "content": content,
            "metadata": metadata or {},
            "status": "success"
        }
