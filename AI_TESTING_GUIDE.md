# 🧪 AI Features Testing Guide

Complete guide to test all AI-powered features in BluePeak Compass.

## Prerequisites

✅ **Before Testing:**
1. Backend running on http://localhost:8000
2. Frontend running on http://localhost:3000
3. API keys configured in `backend/.env`:
   - `ANTHROPIC_API_KEY` - Your Claude API key
   - `SUPABASE_URL` & `SUPABASE_KEY` - Your Supabase credentials

## 🎯 Testing Checklist

### ✅ Step 1: Verify API Keys Are Working

**Test Backend Health:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","environment":"development"}
```

**Test API Documentation:**
- Open: http://localhost:8000/api/v1/docs
- You should see interactive Swagger UI with all endpoints

---

## 🤖 Test 1: Chat with RAG Assistant (Most Important!)

### **Via Web Interface (Easiest)**

1. **Open Frontend:**
   ```
   http://localhost:3000/chat
   ```

2. **Try These Questions:**
   ```
   - "What are the latest trends in AI?"
   - "Tell me about competitive intelligence"
   - "What features should I focus on?"
   - "Analyze market opportunities"
   ```

3. **What to Expect:**
   - You should get intelligent, contextual responses from Claude
   - Responses will be conversational and helpful
   - May include suggestions and follow-up actions

### **Via API (Advanced)**

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the top AI trends in 2024?",
    "context_ids": []
  }'
```

**Expected Response:**
```json
{
  "message": "Based on current data, here are the top AI trends...",
  "conversation_id": "uuid-here",
  "sources": [...],
  "suggested_actions": [...]
}
```

---

## 📊 Test 2: Competitor Analysis Agent

### **Via Web Interface**

1. **Go to Competitors Page:**
   ```
   http://localhost:3000/competitors
   ```

2. **Create a Test Competitor:**
   - Click "Add Competitor"
   - Fill in details:
     - Name: "TechCorp AI"
     - Industry: "Technology"
     - Website: "https://techcorp.ai"
     - Description: "Leading AI platform"

3. **Trigger AI Analysis:**
   - Click "Analyze" button on the competitor
   - Watch the AI agent analyze the competitor

### **Via API**

```bash
# First, create a competitor
curl -X POST http://localhost:8000/api/v1/competitors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Innovations Inc",
    "website": "https://aiinnovations.com",
    "description": "Cutting-edge AI research company",
    "industry": "Technology",
    "status": "active"
  }'

# Copy the competitor ID from response, then analyze it
curl -X POST "http://localhost:8000/api/v1/competitors/COMPETITOR_ID/analyze?analysis_type=comprehensive"
```

**Expected Output:**
- Detailed SWOT analysis
- Market positioning insights
- Competitive advantages
- Threat assessment
- Strategic recommendations

---

## 🔍 Test 3: Market Trend Discovery

### **Via Web Interface**

1. **Go to Trends Page:**
   ```
   http://localhost:3000/trends
   ```

2. **Discover New Trends:**
   - Click "Discover Trends" button
   - Select industry: "Technology"
   - Select timeframe: "30 days"
   - Click "Analyze"

### **Via API**

```bash
curl -X POST "http://localhost:8000/api/v1/trends/discover?industry=Technology&timeframe=30_days"
```

**Expected Output:**
- Emerging trends with confidence scores
- Growth predictions
- Market implications
- Strategic opportunities

---

## 📄 Test 4: Automated Report Generation

### **Via Web Interface**

1. **Go to Reports Page:**
   ```
   http://localhost:3000/reports
   ```

2. **Generate New Report:**
   - Click "Generate New Report"
   - Select report type: "Comprehensive"
   - Click "Generate"
   - Wait for AI to create the report

3. **View Report:**
   - Click on the generated report
   - Read the AI-generated executive summary
   - Explore detailed analysis sections

### **Via API**

```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate?report_type=comprehensive&industry=Technology"
```

**Expected Output:**
```json
{
  "report_id": "uuid",
  "report": {
    "title": "Comprehensive Market Analysis",
    "content": "# Executive Summary\n\n...",
    "summary": "Brief overview...",
    ...
  },
  "message": "Report generated successfully"
}
```

---

## 🎨 Test 5: Multi-Agent Workflow

**This tests all agents working together!**

### **Complete Workflow Test**

```bash
# 1. Create a competitor
COMPETITOR_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/competitors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "NextGen AI",
    "industry": "Technology",
    "description": "Revolutionary AI platform",
    "status": "monitoring"
  }')

echo "Created competitor: $COMPETITOR_RESPONSE"

# 2. Ask the chat assistant about it
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I know about AI competitors in the market?"
  }'

# 3. Discover related trends
curl -X POST "http://localhost:8000/api/v1/trends/discover?industry=Technology"

# 4. Generate a comprehensive report
curl -X POST "http://localhost:8000/api/v1/reports/generate?report_type=comprehensive"
```

---

## 📈 Test 6: Analytics & Insights

### **View Dashboard Metrics**

```bash
curl http://localhost:8000/api/v1/analytics/metrics
```

**Or visit:**
```
http://localhost:3000
```

**Expected to see:**
- Total competitors count
- Active trends
- Recent findings
- Sentiment analysis
- Top industries

---

## 🔬 Advanced Testing

### **Test Individual AI Agents**

Each agent can be tested through the chat interface by asking specific questions:

**Competitive Intelligence Agent:**
```
"Analyze the competitive landscape for AI platforms"
```

**Market Trend Analyst:**
```
"What are emerging trends in machine learning?"
```

**Social Listening Agent:**
```
"What's the sentiment around AI in social media?"
```

**Content Analyzer:**
```
"Summarize this market research: [paste content]"
```

**Synthesis & Reporting:**
```
"Generate an executive summary of current market conditions"
```

---

## 🐛 Troubleshooting

### **Issue: No AI Response**

**Check:**
1. API key is correctly set in `.env`
2. Backend logs show no errors:
   ```bash
   # Check backend logs in terminal
   ```
3. Test Claude API directly:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: YOUR_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{
       "model": "claude-3-5-sonnet-20241022",
       "max_tokens": 100,
       "messages": [{"role": "user", "content": "Hello"}]
     }'
   ```

### **Issue: Database Errors**

**Check:**
1. Supabase credentials are correct
2. Database schema is created (run `database/schema.sql` in Supabase)
3. Test connection:
   ```bash
   curl -X GET "YOUR_SUPABASE_URL/rest/v1/competitors" \
     -H "apikey: YOUR_SUPABASE_KEY"
   ```

### **Issue: Slow Responses**

**Normal behavior:**
- First AI response: 2-5 seconds
- Complex analysis: 5-10 seconds
- Report generation: 10-20 seconds

This is expected as Claude API processes requests.

---

## ✅ Success Indicators

**You'll know AI is working when you see:**

1. **Chat responses** are contextual and intelligent (not canned responses)
2. **Competitor analysis** provides detailed SWOT and insights
3. **Trend discovery** returns emerging patterns with confidence scores
4. **Reports** are comprehensive with executive summaries
5. **Backend logs** show agent initialization messages

---

## 📊 Performance Monitoring

### **Track API Usage**

Monitor your Claude API usage at:
```
https://console.anthropic.com/usage
```

### **Estimated Costs**

- Chat message: ~$0.001 - $0.003
- Competitor analysis: ~$0.01 - $0.03
- Report generation: ~$0.02 - $0.05

**$150 budget should handle:**
- 5,000+ chat messages
- 1,500+ competitor analyses
- 3,000+ trend discoveries
- 3,000+ reports

---

## 🎯 Quick Test Script

Run this to test everything at once:

```bash
#!/bin/bash
echo "🧪 Testing BluePeak Compass AI Features..."

# Test 1: Health check
echo "\n✓ Test 1: Backend Health"
curl -s http://localhost:8000/health

# Test 2: Chat
echo "\n✓ Test 2: Chat AI"
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?"}' \
  | python3 -m json.tool | head -20

# Test 3: Analytics
echo "\n✓ Test 3: Analytics"
curl -s http://localhost:8000/api/v1/analytics/metrics | python3 -m json.tool

echo "\n✅ All tests complete!"
```

Save as `test_ai.sh`, make executable, and run:
```bash
chmod +x test_ai.sh
./test_ai.sh
```

---

## 🚀 Next Steps After Testing

Once AI features are confirmed working:

1. **Generate Dummy Data:**
   ```bash
   cd scripts
   python generate_dummy_data.py
   ```

2. **Explore Full Platform:**
   - Test all dashboard features
   - Try different chat queries
   - Generate multiple reports
   - Analyze competitors

3. **Customize:**
   - Add your real competitors
   - Define industry-specific trends
   - Configure integrations (Slack/Email)

---

## 📞 Need Help?

- **API Docs:** http://localhost:8000/api/v1/docs
- **Backend Logs:** Check terminal running backend
- **Frontend Logs:** Open browser DevTools (F12) → Console
- **Claude API Status:** https://status.anthropic.com/

---

**Happy Testing! 🎉**

Your AI-powered competitive intelligence platform is ready to use!
