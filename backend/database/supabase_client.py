"""
Supabase database client and operations
"""
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import app_logger


class SupabaseClient:
    """Wrapper for Supabase operations"""

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        app_logger.info("Supabase client initialized")

    # Competitor Operations
    async def get_competitors(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch all competitors with optional filters"""
        try:
            query = self.client.table("competitors").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            response = query.execute()
            return response.data
        except Exception as e:
            app_logger.error(f"Error fetching competitors: {e}")
            return []

    async def get_competitor_by_id(self, competitor_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single competitor by ID"""
        try:
            response = self.client.table("competitors").select("*").eq("id", competitor_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error fetching competitor {competitor_id}: {e}")
            return None

    async def create_competitor(self, competitor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new competitor"""
        try:
            response = self.client.table("competitors").insert(competitor_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error creating competitor: {e}")
            return None

    async def update_competitor(self, competitor_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing competitor"""
        try:
            response = self.client.table("competitors").update(update_data).eq("id", competitor_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error updating competitor {competitor_id}: {e}")
            return None

    # Trend Operations
    async def get_trends(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch all trends with optional filters"""
        try:
            query = self.client.table("trends").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            response = query.order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            app_logger.error(f"Error fetching trends: {e}")
            return []

    async def create_trend(self, trend_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new trend"""
        try:
            response = self.client.table("trends").insert(trend_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error creating trend: {e}")
            return None

    # Research Finding Operations
    async def get_findings(self, competitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch research findings, optionally filtered by competitor"""
        try:
            query = self.client.table("research_findings").select("*")

            if competitor_id:
                query = query.eq("competitor_id", competitor_id)

            response = query.order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            app_logger.error(f"Error fetching findings: {e}")
            return []

    async def create_finding(self, finding_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new research finding"""
        try:
            response = self.client.table("research_findings").insert(finding_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error creating finding: {e}")
            return None

    # Report Operations
    async def get_reports(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch generated reports"""
        try:
            response = self.client.table("reports").select("*").order("created_at", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            app_logger.error(f"Error fetching reports: {e}")
            return []

    async def create_report(self, report_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new report"""
        try:
            response = self.client.table("reports").insert(report_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error creating report: {e}")
            return None

    # Conversation Operations
    async def get_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch chat conversations for a user"""
        try:
            response = self.client.table("conversations").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
            return response.data
        except Exception as e:
            app_logger.error(f"Error fetching conversations: {e}")
            return []

    async def create_conversation(self, conversation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new conversation"""
        try:
            response = self.client.table("conversations").insert(conversation_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error creating conversation: {e}")
            return None

    async def update_conversation(self, conversation_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a conversation"""
        try:
            response = self.client.table("conversations").update(update_data).eq("id", conversation_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            app_logger.error(f"Error updating conversation: {e}")
            return None


# Global instance
supabase_client = SupabaseClient()
