# Railway Deployment - Step by Step Guide

## Step 1: Create a New Project

1. Go to https://railway.app/dashboard
2. Click **"+ New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository from the list
5. Railway will start analyzing your repo

## Step 2: Configure the Service

After Railway detects your repo:

1. Railway might show multiple directories - select the **root** of your project
2. It should detect the `railway.toml` and `Procfile` automatically
3. Click on the service that was created

## Step 3: Add Environment Variables (IMPORTANT!)

Click on the **"Variables"** tab in your Railway project and add these:

### Required Variables:

```bash
# Claude API (Get from: https://console.anthropic.com/)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Supabase (Get from your Supabase dashboard)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

# Security (Generate a random string)
SECRET_KEY=your-random-secret-key-here-make-it-long-and-random

# Environment
ENVIRONMENT=production
DEBUG=False

# CORS (Will update after getting Vercel URL)
CORS_ORIGINS=https://localhost:3000

# Redis (We'll add Railway Redis next)
REDIS_HOST=redis.railway.internal
REDIS_PORT=6379
REDIS_DB=0

# API Settings
API_HOST=0.0.0.0
API_PREFIX=/api/v1
LOG_LEVEL=INFO
```

### Optional Variables (if you have them):

```bash
# Slack Integration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret

# SendGrid Email
SENDGRID_API_KEY=SG.xxxxx
FROM_EMAIL=noreply@yourdomain.com
```

**How to add variables:**
1. Click **"+ New Variable"** or use the **"Raw Editor"**
2. Paste the variables above
3. Replace the values with your actual keys
4. Click **"Add"** or **"Save"**

## Step 4: Add Redis Database (Recommended)

1. In your Railway project, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add Redis"**
4. Railway will automatically create a Redis instance
5. It will add `REDIS_URL` variable automatically
6. You can keep `REDIS_HOST=redis.railway.internal` if using internal connection

## Step 5: Deploy

1. Once variables are set, Railway will automatically start deploying
2. Watch the **"Deployments"** tab for progress
3. You'll see the build logs in real-time
4. Wait for it to show **"Success"** (this may take 3-5 minutes)

## Step 6: Get Your Backend URL

1. Go to the **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Railway will give you a URL like: `https://your-app.up.railway.app`
5. **Copy this URL** - you'll need it for Vercel!

## Step 7: Test Your Backend

Visit these URLs to verify it's working:

```
https://your-app.up.railway.app/health
https://your-app.up.railway.app/api/v1/health
https://your-app.up.railway.app/api/v1/docs
```

You should see:
- `/health` → `{"status": "healthy", "environment": "production"}`
- `/api/v1/docs` → Swagger API documentation

## Step 8: Update CORS for Vercel (Do this after deploying to Vercel)

Once you have your Vercel URL, come back to Railway:

1. Go to **"Variables"** tab
2. Find `CORS_ORIGINS`
3. Update it to include your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
   ```
4. Save - Railway will automatically redeploy

## Common Issues & Solutions

### ❌ Build fails with "requirements.txt not found"
**Solution:** Check that your `railway.toml` has:
```toml
buildCommand = "pip install -r backend/requirements.txt"
```

### ❌ App crashes on startup
**Solution:**
- Check the logs in Railway dashboard
- Verify all required environment variables are set
- Ensure `ANTHROPIC_API_KEY` and Supabase credentials are correct

### ❌ "Module not found" errors
**Solution:** Make sure all dependencies are in `backend/requirements.txt`

### ❌ CORS errors when calling from frontend
**Solution:** Update `CORS_ORIGINS` environment variable to include your frontend URL

## Environment Variables Quick Reference

Here's what each variable does:

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude API key for AI features | `sk-ant-xxx` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase anonymous key | `eyJhbGci...` |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | `eyJhbGci...` |
| `SECRET_KEY` | For JWT tokens and encryption | Random long string |
| `CORS_ORIGINS` | Allowed frontend URLs | `https://app.vercel.app` |
| `ENVIRONMENT` | Deployment environment | `production` |
| `DEBUG` | Enable debug mode | `False` |
| `REDIS_HOST` | Redis server host | `redis.railway.internal` |

## Auto-Deployment Setup

Railway is already configured for auto-deployment!

Every time you push to your `main` branch:
1. Railway detects the changes
2. Automatically builds the new version
3. Deploys it with zero downtime
4. You get a notification when it's live

## Viewing Logs

To see what's happening:
1. Go to your Railway project
2. Click on your service
3. Click on **"Deployments"**
4. Click on the latest deployment
5. View real-time logs

## Cost

Railway pricing:
- **$5 free credit per month**
- After that: Pay as you go
- Estimated cost: **$5-15/month** for moderate usage

## Next Steps

1. ✅ Deploy backend to Railway (you're doing this now!)
2. ⬜ Deploy frontend to Vercel
3. ⬜ Update CORS settings with Vercel URL
4. ⬜ Test the full application

---

**Need help?** Check the Railway logs or ask me!
