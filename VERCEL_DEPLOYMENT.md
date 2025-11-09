# Vercel + Railway Deployment Guide

This guide will help you deploy BluePeak Compass with:
- **Frontend (Next.js)** on Vercel
- **Backend (FastAPI)** on Railway

Both platforms support automatic deployments from GitHub!

## Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Railway account (sign up at https://railway.app)
- Your Supabase credentials
- Your Anthropic API key

## Part 1: Deploy Backend to Railway

### Step 1: Push Your Code to GitHub

```bash
git add .
git commit -m "Add deployment configurations"
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select your repository
6. Railway will automatically detect the configuration from `railway.toml` and `Procfile`

### Step 3: Configure Environment Variables in Railway

In your Railway project dashboard, go to Variables and add:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
SECRET_KEY=your_secret_key_here
REDIS_HOST=redis.railway.internal
REDIS_PORT=6379
PORT=8000
```

### Step 4: Add Redis to Railway (Optional but Recommended)

1. In your Railway project, click "New"
2. Select "Database" → "Add Redis"
3. Railway will automatically set up Redis and configure the connection
4. Update `REDIS_HOST` to use the internal Railway Redis URL

### Step 5: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Once deployed, copy your backend URL (e.g., `https://your-app.railway.app`)
3. Note: Railway provides the full URL - you'll need this for Vercel

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Project

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Vercel will auto-detect Next.js

### Step 2: Configure Build Settings

Vercel should automatically detect the settings from `vercel.json`, but verify:

- **Framework Preset**: Next.js
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Step 3: Configure Environment Variables

In your Vercel project settings, add these environment variables:

```env
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app/api/v1
NEXT_PUBLIC_WS_URL=wss://your-railway-app.railway.app/ws
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Important:** Replace `your-railway-app.railway.app` with your actual Railway backend URL!

### Step 4: Deploy

1. Click "Deploy"
2. Vercel will build and deploy your frontend
3. Once deployed, you'll get a URL like `https://your-app.vercel.app`

## Part 3: Enable Auto-Deployments

Both platforms are now set up for automatic deployments!

### Vercel Auto-Deploy
- Every push to `main` branch will trigger a new deployment
- Pull requests get preview deployments automatically
- You can configure which branches trigger deployments in Project Settings

### Railway Auto-Deploy
- Every push to `main` branch will trigger a new deployment
- You can configure deployment triggers in Railway settings

## Part 4: Update CORS Settings (Important!)

You need to update your backend to allow requests from your Vercel domain.

1. SSH into your Railway deployment or update locally
2. Update `backend/app/main.py` to include your Vercel URL in CORS origins:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Commit and push the changes - Railway will auto-deploy!

## Testing Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Check that the frontend loads correctly
3. Test API connectivity by trying to load data
4. Check browser console for any CORS or connection errors

## Troubleshooting

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` in Vercel environment variables
- Check CORS settings in backend
- Ensure Railway backend is running (check Railway logs)

### Railway deployment fails
- Check Railway build logs
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies

### WebSocket connection issues
- Verify `NEXT_PUBLIC_WS_URL` uses `wss://` (not `ws://`)
- Check Railway allows WebSocket connections (it does by default)

## Viewing Logs

### Vercel Logs
1. Go to your project in Vercel dashboard
2. Click "Deployments"
3. Click on a deployment to see logs

### Railway Logs
1. Go to your project in Railway dashboard
2. Click on your service
3. View logs in real-time

## Cost Estimates

### Vercel
- Free tier: Generous limits for hobby projects
- Pro: $20/month (if you need more)

### Railway
- $5/month free credit
- Pay-as-you-go after that
- Estimated cost: $5-20/month depending on usage

## Custom Domains (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Railway
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## Updates and Rollbacks

### Deploy New Changes
```bash
git add .
git commit -m "Your update message"
git push origin main
```
Both platforms will automatically deploy!

### Rollback
- **Vercel**: Go to Deployments → Click on previous deployment → "Promote to Production"
- **Railway**: Go to Deployments → Click on previous deployment → "Redeploy"

## Environment-Specific Tips

### Development
- Use local environment for development
- Push to a `develop` branch to test before merging to `main`

### Staging
- Create a separate Vercel project for staging
- Link it to a `staging` branch in GitHub
- Use separate Railway project or service for staging backend

### Production
- Use `main` branch for production deployments
- Enable Vercel's protection for production deployments
- Set up monitoring and alerts

## Next Steps

1. Set up monitoring (Railway and Vercel provide basic monitoring)
2. Configure custom domains if needed
3. Set up error tracking (e.g., Sentry)
4. Configure analytics
5. Set up automated backups for your database

## Support

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- For issues specific to this project, check the main README.md

---

**You're all set!** Every time you push to GitHub, both your frontend and backend will automatically deploy.
