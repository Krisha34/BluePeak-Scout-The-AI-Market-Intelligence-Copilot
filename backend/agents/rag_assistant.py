"""
RAG Query Assistant Agent - Conversational interface for research queries
"""
from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from app.core.logger import app_logger
import json


class RAGQueryAssistantAgent(BaseAgent):
    """
    Specialized agent for RAG-powered conversational queries
    """

    def __init__(self):
        super().__init__(
            name="RAG Query Assistant Agent",
            description="Provides conversational interface for research queries using RAG (Retrieval-Augmented Generation)"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute RAG query

        Args:
            task: Contains query, conversation_history, context_ids

        Returns:
            Response with sources and suggested actions
        """
        query = task.get("query", "")
        conversation_history = task.get("conversation_history", [])
        context_ids = task.get("context_ids", [])

        app_logger.info(f"Processing RAG query: {query[:100]}")

        response = await self.process_query(query, conversation_history, context_ids)

        return self.format_response(
            content=response["answer"],
            metadata={
                "sources": response.get("sources", []),
                "suggested_actions": response.get("suggested_actions", []),
                "confidence": response.get("confidence", 0.8)
            }
        )

    async def process_query(self, query: str, history: List[Dict[str, Any]], context_ids: List[str]) -> Dict[str, Any]:
        """Process a research query with RAG"""

        # In a real implementation, this would:
        # 1. Embed the query
        # 2. Search vector database
        # 3. Retrieve relevant documents
        # 4. Generate answer with sources

        prompt = f"""You are a research assistant for competitive intelligence and market research.

User Query: {query}

Conversation History:
{json.dumps(history[-3:] if history else [], indent=2)}

Context IDs: {context_ids}

Based on the query, provide:
1. A comprehensive answer
2. Relevant sources (competitors, trends, reports)
3. Follow-up suggestions
4. Related topics to explore

Since this is a demo, generate realistic responses based on typical competitive intelligence scenarios.

Format response as JSON:
{{
    "answer": "Detailed answer to the query...",
    "sources": [
        {{
            "type": "competitor/trend/report",
            "id": "source_id",
            "title": "Source title",
            "relevance": 0.95,
            "excerpt": "Relevant excerpt..."
        }}
    ],
    "suggested_actions": [
        "Action 1",
        "Action 2"
    ],
    "related_topics": [
        "Topic 1",
        "Topic 2"
    ],
    "confidence": 0.9
}}"""

        response_text = await self.invoke_llm(prompt)

        try:
            # Clean up response text - remove markdown code blocks if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]  # Remove ```

            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove trailing ```

            cleaned_text = cleaned_text.strip()

            response_data = json.loads(cleaned_text)
            return response_data
        except Exception as e:
            app_logger.error(f"Failed to parse JSON response: {e}")
            app_logger.debug(f"Raw response: {response_text[:500]}")
            return {
                "answer": response_text,
                "sources": [],
                "suggested_actions": [],
                "confidence": 0.7
            }

    async def search_knowledge_base(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information"""

        # This would integrate with Chroma vector database
        app_logger.info(f"Searching knowledge base: {query}")

        # Mock search results for demo
        return [
            {
                "id": "doc_1",
                "content": "Sample relevant content...",
                "metadata": {"source": "competitor_analysis", "date": "2024-01-15"},
                "score": 0.92
            }
        ]

    async def generate_contextual_response(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Generate response based on retrieved documents"""

        prompt = f"""Answer this query using the provided context:

Query: {query}

Retrieved Context:
{json.dumps(retrieved_docs, indent=2)}

Provide a clear, comprehensive answer that:
- Directly addresses the query
- Cites specific sources
- Provides actionable insights
- Suggests next steps

If the context doesn't fully answer the query, acknowledge this and provide the best possible answer."""

        response = await self.invoke_llm(prompt)
        return response

    async def suggest_follow_up_questions(self, query: str, response: str) -> List[str]:
        """Suggest relevant follow-up questions"""

        prompt = f"""Based on this conversation:

User Query: {query}
Assistant Response: {response[:500]}

Suggest 3-5 relevant follow-up questions that would help the user:
- Go deeper into the topic
- Explore related areas
- Get actionable insights
- Compare alternatives

Return as JSON array of questions."""

        suggestions = await self.invoke_llm(prompt)

        try:
            questions = json.loads(suggestions)
            return questions if isinstance(questions, list) else []
        except:
            return [
                "Can you provide more details?",
                "What are the implications of this?",
                "How does this compare to competitors?"
            ]

    async def clarify_ambiguous_query(self, query: str) -> Dict[str, Any]:
        """Handle ambiguous or unclear queries"""

        prompt = f"""This query may be ambiguous: "{query}"

Provide:
1. Possible interpretations
2. Clarifying questions to ask the user
3. Best guess at user intent
4. Suggested refined queries

Format as JSON."""

        clarification = await self.invoke_llm(prompt)

        return {
            "needs_clarification": True,
            "clarification_data": clarification
        }

    async def summarize_conversation(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Summarize a conversation thread"""

        prompt = f"""Summarize this conversation:

{json.dumps(conversation_history, indent=2)}

Provide:
- Main topics discussed
- Key insights shared
- Questions answered
- Action items
- Suggested next steps

Format as concise summary."""

        summary = await self.invoke_llm(prompt)
        return summary
