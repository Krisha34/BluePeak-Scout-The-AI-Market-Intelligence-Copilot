# BluePeak Compass API Documentation

Complete API reference for BluePeak Compass platform.

## Base URL

```
http://localhost:8000/api/v1
```

Production: `https://your-domain.com/api/v1`

## Authentication

Currently, the API does not require authentication for demo purposes. In production, implement JWT-based authentication:

```http
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses follow this structure:

**Success Response:**
```json
{
  "data": { ... },
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "status": "error"
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per IP

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Competitors API

### List Competitors

Get all competitors with optional filtering.

**Endpoint:** `GET /competitors`

**Query Parameters:**
- `status` (string, optional): Filter by status (active, inactive, monitoring)
- `industry` (string, optional): Filter by industry
- `limit` (integer, optional): Max results (default: 50, max: 100)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/competitors?status=active&limit=10"
```

**Example Response:**
```json
[
  {
    "id": "uuid",
    "name": "TechVision AI",
    "website": "https://techvision-ai.com",
    "description": "Leading AI analytics platform",
    "industry": "Technology",
    "founded_year": 2018,
    "headquarters": "San Francisco, CA",
    "employee_count": 450,
    "status": "active",
    "monitoring_score": 0.87,
    "last_analyzed": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Competitor

Retrieve details for a specific competitor.

**Endpoint:** `GET /competitors/{competitor_id}`

**Example Response:**
```json
{
  "id": "uuid",
  "name": "TechVision AI",
  ...
}
```

### Create Competitor

Add a new competitor to monitor.

**Endpoint:** `POST /competitors`

**Request Body:**
```json
{
  "name": "New Competitor",
  "website": "https://example.com",
  "description": "Company description",
  "industry": "Technology",
  "founded_year": 2020,
  "headquarters": "Austin, TX",
  "employee_count": 100,
  "status": "active"
}
```

**Response:** `201 Created` with created competitor object

### Analyze Competitor

Trigger AI analysis of a competitor.

**Endpoint:** `POST /competitors/{competitor_id}/analyze`

**Query Parameters:**
- `analysis_type` (string): Type of analysis (comprehensive, quick, deep)

**Example Response:**
```json
{
  "competitor_id": "uuid",
  "analysis": {
    "agent": "Competitive Intelligence Agent",
    "content": "Analysis results...",
    "metadata": {
      "competitor": "TechVision AI",
      "analysis_type": "comprehensive"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Competitor Findings

Get research findings for a specific competitor.

**Endpoint:** `GET /competitors/{competitor_id}/findings`

**Query Parameters:**
- `limit` (integer): Max results (default: 20)

---

## Trends API

### List Trends

Get all market trends with filtering.

**Endpoint:** `GET /trends`

**Query Parameters:**
- `status` (string): Filter by status (emerging, growing, declining, stable)
- `industry` (string): Filter by industry
- `limit` (integer): Max results

**Example Response:**
```json
[
  {
    "id": "uuid",
    "title": "Generative AI in Enterprise",
    "description": "Rapid adoption of generative AI...",
    "industry": "Technology",
    "status": "growing",
    "confidence_score": 0.92,
    "keywords": ["ai", "llm", "enterprise"],
    "mention_count": 1247,
    "growth_rate": 156.3,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T00:00:00Z"
  }
]
```

### Create Trend

Manually add a new trend.

**Endpoint:** `POST /trends`

**Request Body:**
```json
{
  "title": "Trend Title",
  "description": "Trend description",
  "industry": "Technology",
  "status": "emerging",
  "confidence_score": 0.85,
  "keywords": ["keyword1", "keyword2"]
}
```

### Discover Trends

Use AI to discover new market trends.

**Endpoint:** `POST /trends/discover`

**Query Parameters:**
- `industry` (string, required): Industry to analyze
- `timeframe` (string): Analysis timeframe (7_days, 30_days, 90_days)

**Example Response:**
```json
{
  "industry": "Technology",
  "timeframe": "30_days",
  "analysis": {
    "agent": "Market Trend Analyst Agent",
    "content": "Discovered trends...",
    "metadata": {...}
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Predict Trend Trajectory

Get AI predictions for a trend's future.

**Endpoint:** `GET /trends/{trend_id}/trajectory`

**Example Response:**
```json
{
  "trend_id": "uuid",
  "prediction": {
    "growth_projection": "...",
    "adoption_curve_stage": "early_majority",
    "confidence": 0.85
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Chat API

### Send Message

Send a message and get AI-powered response.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "message": "What are the top trends in AI?",
  "conversation_id": "uuid",  // optional
  "context_ids": ["competitor_id", "trend_id"]  // optional
}
```

**Response:**
```json
{
  "message": "Based on current data, the top trends...",
  "conversation_id": "uuid",
  "sources": [
    {
      "type": "trend",
      "id": "uuid",
      "title": "Generative AI in Enterprise",
      "relevance": 0.95
    }
  ],
  "suggested_actions": [
    "Generate detailed report",
    "Analyze competitor strategies"
  ]
}
```

### List Conversations

Get user's conversation history.

**Endpoint:** `GET /chat/conversations`

**Query Parameters:**
- `user_id` (string): User identifier (default: default_user)
- `limit` (integer): Max results

### Get Conversation

Retrieve a specific conversation.

**Endpoint:** `GET /chat/conversations/{conversation_id}`

---

## Reports API

### List Reports

Get all generated reports.

**Endpoint:** `GET /reports`

**Query Parameters:**
- `limit` (integer): Max results

**Example Response:**
```json
[
  {
    "id": "uuid",
    "title": "Q4 2024 Competitive Analysis",
    "report_type": "competitive_analysis",
    "content": "Full report content...",
    "summary": "Executive summary...",
    "competitor_ids": ["uuid1", "uuid2"],
    "trend_ids": ["uuid3"],
    "generated_by": "ai_agent",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Generate Report

Create a new AI-generated report.

**Endpoint:** `POST /reports/generate`

**Query Parameters:**
- `report_type` (string): Type of report (comprehensive, competitor_analysis, market_trends)
- `competitor_ids` (array): Competitors to include
- `trend_ids` (array): Trends to include
- `industry` (string): Industry focus

**Example Response:**
```json
{
  "report_id": "uuid",
  "report": {...},
  "message": "Report generated successfully"
}
```

### Export Report

Export report in different formats.

**Endpoint:** `POST /reports/{report_id}/export`

**Query Parameters:**
- `format` (string): Export format (pdf, email, slack, dashboard)

---

## Analytics API

### Get Metrics

Get overall platform metrics.

**Endpoint:** `GET /analytics/metrics`

**Example Response:**
```json
{
  "total_competitors": 10,
  "active_trends": 8,
  "findings_this_week": 47,
  "reports_generated": 4,
  "sentiment_breakdown": {
    "positive": 25,
    "neutral": 15,
    "negative": 7
  },
  "top_industries": [
    {"name": "Technology", "count": 10}
  ]
}
```

### Get Dashboard Data

Get comprehensive dashboard overview.

**Endpoint:** `GET /analytics/dashboard`

---

## Integrations API

### Get Integration Settings

Retrieve current integration configuration.

**Endpoint:** `GET /integrations`

### Update Integration Settings

Update integration configuration.

**Endpoint:** `PUT /integrations`

**Request Body:**
```json
{
  "slack": {
    "enabled": true,
    "channel_id": "C123456",
    "notification_types": ["new_findings", "trend_alerts"]
  },
  "email": {
    "enabled": true,
    "recipients": ["user@example.com"],
    "frequency": "daily"
  }
}
```

### Test Slack Integration

Send test message to Slack.

**Endpoint:** `POST /integrations/slack/test`

### Test Email Integration

Send test email.

**Endpoint:** `POST /integrations/email/test`

---

## WebSocket API

### Real-time Updates

Connect to WebSocket for real-time notifications.

**Endpoint:** `WS /ws/updates`

**Query Parameters:**
- `user_id` (string): User identifier

**Message Types:**

**Connection:**
```json
{
  "type": "connection",
  "data": {
    "status": "connected",
    "user_id": "default"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Ping/Pong:**
```json
// Client -> Server
{"type": "ping"}

// Server -> Client
{
  "type": "pong",
  "data": {"timestamp": "..."}
}
```

**Subscription:**
```json
// Client -> Server
{
  "type": "subscribe",
  "data": {
    "topics": ["competitors", "trends", "reports"]
  }
}
```

**Updates:**
```json
{
  "type": "competitor_update",
  "data": {
    "competitor": {...},
    "changes": [...]
  },
  "timestamp": "..."
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Code Examples

### Python

```python
import requests

API_URL = "http://localhost:8000/api/v1"

# Get competitors
response = requests.get(f"{API_URL}/competitors")
competitors = response.json()

# Send chat message
response = requests.post(
    f"{API_URL}/chat",
    json={
        "message": "What are the latest trends?",
        "context_ids": []
    }
)
chat_response = response.json()
```

### JavaScript

```javascript
const API_URL = 'http://localhost:8000/api/v1';

// Get competitors
const competitors = await fetch(`${API_URL}/competitors`)
  .then(res => res.json());

// Send chat message
const chatResponse = await fetch(`${API_URL}/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What are the latest trends?',
    context_ids: []
  })
}).then(res => res.json());
```

### cURL

```bash
# Get competitors
curl -X GET "http://localhost:8000/api/v1/competitors"

# Generate report
curl -X POST "http://localhost:8000/api/v1/reports/generate?report_type=comprehensive"

# Send chat message
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the latest trends?"}'
```

---

For interactive API documentation, visit: `http://localhost:8000/api/v1/docs`
