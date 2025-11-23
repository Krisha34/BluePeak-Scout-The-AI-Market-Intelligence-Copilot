"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CompetitorStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MONITORING = "monitoring"


class TrendStatus(str, Enum):
    EMERGING = "emerging"
    GROWING = "growing"
    DECLINING = "declining"
    STABLE = "stable"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


# Competitor Models
class CompetitorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    website: Optional[str] = None
    description: Optional[str] = None
    industry: str
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    employee_count: Optional[int] = None
    status: CompetitorStatus = CompetitorStatus.ACTIVE


class CompetitorCreate(CompetitorBase):
    pass


class CompetitorUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[CompetitorStatus] = None


class CompetitorResponse(CompetitorBase):
    id: str
    created_at: datetime
    updated_at: datetime
    monitoring_score: float = 0.0
    last_analyzed: Optional[datetime] = None

    class Config:
        from_attributes = True


# Trend Models
class TrendBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    industry: str
    status: TrendStatus = TrendStatus.EMERGING
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    keywords: List[str] = []


class TrendCreate(TrendBase):
    pass


class TrendResponse(TrendBase):
    id: str
    created_at: datetime
    updated_at: datetime
    mention_count: int = 0
    growth_rate: float = 0.0

    class Config:
        from_attributes = True


# Research Finding Models
class ResearchFindingBase(BaseModel):
    competitor_id: str
    finding_type: str
    title: str
    content: str
    source_url: Optional[str] = None
    sentiment: SentimentType = SentimentType.NEUTRAL
    importance_score: float = Field(..., ge=0.0, le=1.0)


class ResearchFindingCreate(ResearchFindingBase):
    pass


class ResearchFindingResponse(ResearchFindingBase):
    id: str
    created_at: datetime
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


# Report Models
class ReportBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    report_type: str
    content: str
    summary: str
    competitor_ids: List[str] = []
    trend_ids: List[str] = []


class ReportCreate(ReportBase):
    pass


class ReportResponse(ReportBase):
    id: str
    created_at: datetime
    generated_by: str = "ai_agent"

    class Config:
        from_attributes = True


# Chat Models
class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context_ids: List[str] = []  # IDs of competitors/trends for context


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: List[Dict[str, Any]] = []
    suggested_actions: List[str] = []


# Integration Models
class SlackIntegration(BaseModel):
    enabled: bool = False
    channel_id: Optional[str] = None
    webhook_url: Optional[str] = None
    notification_types: List[str] = ["new_findings", "trend_alerts", "reports"]


class EmailIntegration(BaseModel):
    enabled: bool = False
    recipients: List[EmailStr] = []
    frequency: str = "daily"  # daily, weekly, real-time
    notification_types: List[str] = ["reports", "critical_alerts"]


class IntegrationSettings(BaseModel):
    slack: SlackIntegration = SlackIntegration()
    email: EmailIntegration = EmailIntegration()


# Analytics Models
class AnalyticsMetrics(BaseModel):
    total_competitors: int = 0
    active_trends: int = 0
    findings_this_week: int = 0
    reports_generated: int = 0
    sentiment_breakdown: Dict[str, int] = {}
    top_industries: List[Dict[str, Any]] = []


# WebSocket Models
class WSMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
