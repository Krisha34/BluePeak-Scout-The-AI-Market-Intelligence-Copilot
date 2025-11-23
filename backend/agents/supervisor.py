"""
Supervisor Agent - Coordinates all operations and delegates tasks
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from app.core.logger import app_logger
import json


class SupervisorAgent(BaseAgent):
    """
    Supervisor agent that coordinates operations across all specialized agents
    """

    def __init__(self):
        super().__init__(
            name="Supervisor Agent",
            description="Coordinates multi-agent operations, delegates tasks to specialized agents, and synthesizes results"
        )
        self.available_agents = [
            "competitive_intelligence",
            "market_trend_analyst",
            "social_listening",
            "content_analyzer",
            "synthesis_reporting",
            "rag_query_assistant"
        ]

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute supervisor coordination

        Args:
            task: Contains task_type, parameters, and priority

        Returns:
            Coordination plan and delegated tasks
        """
        task_type = task.get("task_type", "unknown")
        app_logger.info(f"Supervisor processing task: {task_type}")

        # Analyze task and create execution plan
        plan = await self.create_execution_plan(task)

        return self.format_response(
            content=json.dumps(plan, indent=2),
            metadata={"plan": plan, "task_type": task_type}
        )

    async def create_execution_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create an execution plan based on task type"""
        task_type = task.get("task_type")

        plans = {
            "competitor_analysis": {
                "agents": ["competitive_intelligence", "content_analyzer", "synthesis_reporting"],
                "sequence": ["gather_data", "analyze_content", "generate_report"],
                "priority": "high"
            },
            "trend_discovery": {
                "agents": ["market_trend_analyst", "social_listening", "synthesis_reporting"],
                "sequence": ["identify_trends", "validate_social", "compile_findings"],
                "priority": "medium"
            },
            "research_query": {
                "agents": ["rag_query_assistant"],
                "sequence": ["search_knowledge_base", "generate_response"],
                "priority": "high"
            },
            "comprehensive_report": {
                "agents": ["competitive_intelligence", "market_trend_analyst", "social_listening", "synthesis_reporting"],
                "sequence": ["gather_all_data", "analyze_trends", "synthesize_report"],
                "priority": "high"
            },
            "social_monitoring": {
                "agents": ["social_listening", "content_analyzer"],
                "sequence": ["monitor_social", "analyze_sentiment"],
                "priority": "medium"
            }
        }

        return plans.get(task_type, {
            "agents": ["competitive_intelligence"],
            "sequence": ["default_analysis"],
            "priority": "low"
        })

    async def delegate_task(self, agent_name: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a specific task to an agent"""
        app_logger.info(f"Delegating task to {agent_name}")

        return {
            "agent": agent_name,
            "task": task_data,
            "status": "delegated",
            "timestamp": "now"
        }

    async def synthesize_results(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize results from multiple agents"""
        prompt = f"""As the Supervisor Agent, synthesize the following results from specialized agents:

{json.dumps(agent_results, indent=2)}

Provide a comprehensive summary that integrates all findings."""

        synthesis = await self.invoke_llm(prompt)

        return self.format_response(
            content=synthesis,
            metadata={"agent_count": len(agent_results)}
        )
