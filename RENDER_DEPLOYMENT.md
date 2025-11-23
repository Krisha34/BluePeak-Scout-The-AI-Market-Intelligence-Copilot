# Render Deployment Guide - Simple & Fast! 🚀

Render is much simpler than Railway for Python apps. No Docker complexity!

## Prerequisites

- GitHub account (you already have this)
- Render account (sign up at https://render.com - free!)
- Your API keys ready

## Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. From Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository (search for "hackethon")
4. Click **"Connect"**

### Step 3: Configure the Service

Fill in these settings:

**Basic Settings:**
- **Name**: `bluepeak-compass-backend` (or any name you like)
- **Region**: Choose closest to you (e.g., Singapore)
- **Branch**: `monesh` (or `main` if you merged)
- **Root Directory**: Leave blank
- **Environment**: `Python 3`
- **Build Command**:
  ```
  pip install -r backend/requirements.txt
  ```
- **Start Command**:
  ```
  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (perfect for testing, $0/month)

### Step 4: Add Environment Variables

Click **"Advanced"** and add these environment variables:

**Required Variables:**

| Key | Value | Where to Get It |
|-----|-------|----------------|
| `ANTHROPIC_API_KEY` | Your Claude API key | https://console.anthropic.com/ |
| `SUPABASE_URL` | Your Supabase URL | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Your Supabase anon key | Supabase Dashboard → Settings → API |
| `SUPABASE_SERVICE_KEY` | Your Supabase service key | Supabase Dashboard → Settings → API |
| `SECRET_KEY` | Random string (use password generator) | Generate a long random string |
| `ENVIRONMENT` | `production` | Just type this |
| `DEBUG` | `False` | Just type this |
| `LOG_LEVEL` | `INFO` | Just type this |
| `API_HOST` | `0.0.0.0` | Just type this |
| `API_PREFIX` | `/api/v1` | Just type this |
| `CORS_ORIGINS` | `http://localhost:3000,https://*.vercel.app` | Just type this |

**Optional (for Redis - skip for now):**
- `REDIS_HOST` = `localhost`
- `REDIS_PORT` = `6379`
- `REDIS_DB` = `0`

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Pull your code from GitHub
   - Install Python dependencies
   - Start your FastAPI server
3. Watch the logs in real-time
4. Wait 3-5 minutes for the first deployment

### Step 6: Get Your URL

Once deployment succeeds:
- Your URL will be shown at the top: `https://your-app.onrender.com`
- Copy this URL - you'll need it for Vercel!

### Step 7: Test Your Backend

Visit these URLs to verify it works:

```
https://your-app.onrender.com/health
https://your-app.onrender.com/api/v1/health
https://your-app.onrender.com/api/v1/docs
```

You should see:
- `/health` → `{"status": "healthy", "environment": "production"}`
- `/api/v1/docs` → Swagger API documentation

## Auto-Deployments

Render automatically deploys when you push to GitHub! 🎉

- Every push to your branch triggers a new deployment
- Zero configuration needed
- You get notifications when deployments complete

## Important Notes

### Free Tier Limitations:
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- Upgrade to paid plan ($7/month) for always-on service

### Update CORS After Vercel Deployment:
Once you deploy to Vercel, come back and update the `CORS_ORIGINS` variable:
1. Go to your service in Render
2. Click **"Environment"**
3. Update `CORS_ORIGINS` to:
   ```
   https://your-app.vercel.app,https://*.vercel.app
   ```
4. Click **"Save Changes"** - Render will redeploy automatically

## Troubleshooting

### Build fails with "requirements.txt not found"
- Make sure the build command is: `pip install -r backend/requirements.txt`
- Check that your branch has the latest code

### Service crashes on startup
- Check the logs in Render dashboard
- Verify all required environment variables are set
- Make sure API keys are correct

### CORS errors from frontend
- Update `CORS_ORIGINS` to include your Vercel URL
- Save changes and wait for redeploy

## Logs

To view logs:
1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. See real-time logs of your application

## Cost

- **Free tier**: $0/month (perfect for testing)
  - 750 hours/month
  - Spins down after inactivity

- **Starter**: $7/month
  - Always on
  - No spin down
  - Better performance

## Next Steps

1. ✅ Deploy backend to Render (you're doing this now!)
2. ⬜ Deploy frontend to Vercel
3. ⬜ Update CORS with Vercel URL
4. ⬜ Test full application

---

**Much simpler than Railway, right?** 😊
