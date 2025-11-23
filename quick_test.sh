#!/bin/bash
echo "🧪 BluePeak Compass - Quick AI Test"
echo "===================================="

# Test 1: Health
echo -e "\n✓ Test 1: Backend Health Check"
curl -s http://localhost:8000/health | python3 -m json.tool

# Test 2: Simple Chat Test
echo -e "\n✓ Test 2: AI Chat Assistant"
echo "Asking: 'What can you help me with?'"
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! What can you help me with in this competitive intelligence platform?"}' \
  | python3 -m json.tool | head -30

# Test 3: Analytics
echo -e "\n✓ Test 3: Platform Analytics"
curl -s http://localhost:8000/api/v1/analytics/metrics | python3 -m json.tool

echo -e "\n===================================="
echo "✅ Quick test complete!"
echo ""
echo "📚 For detailed testing guide, see:"
echo "   AI_TESTING_GUIDE.md"
echo ""
echo "🌐 Access your application at:"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/api/v1/docs"
