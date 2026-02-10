# GCP Deployment Guide - Fun Learn
## Cheapest Option for Gemini 3 Hackathon

**Total Cost: $0** (within free tier limits)

- **Backend**: Cloud Run (Free tier: 2M requests/month)
- **Frontend**: Firebase Hosting (Free tier: 10GB storage, 360MB/day)

---

## Prerequisites

1. GCP Project: `silicon-guru-472717-q9` ✅
2. GitHub repo ready ✅
3. Gemini API key
4. gcloud CLI installed

**Install gcloud CLI** (if not installed):
```powershell
# Download from: https://cloud.google.com/sdk/docs/install
# Or use PowerShell:
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

---

## Step 1: Prepare Backend for Cloud Run

### 1.1 Create Dockerfile

Create `genlearn-ai/backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data/csv data/media secrets

# Expose Cloud Run port
EXPOSE 8080

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 1.2 Create .dockerignore

Create `genlearn-ai/backend/.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.env.local
*.log
.git
.gitignore
README.md
.DS_Store
data/media/*
!data/media/.gitkeep
```

### 1.3 Update Config for Production

No changes needed - your `config.py` already reads from environment variables.

---

## Step 2: Deploy Backend to Cloud Run

### 2.1 Login and Set Project

```powershell
# Login to GCP
gcloud auth login

# Set project
gcloud config set project silicon-guru-472717-q9

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 2.2 Deploy Backend

```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\backend

# Deploy to Cloud Run (this builds and deploys in one command)
gcloud run deploy funlearn-backend `
  --source . `
  --region us-central1 `
  --platform managed `
  --allow-unauthenticated `
  --port 8080 `
  --set-env-vars "APP_ENV=production,DEBUG=false,BACKEND_PORT=8080,AI_PROVIDER=gemini,IMAGE_PROVIDER=gemini,VOICE_TTS_PROVIDER=gcp,VOICE_STT_PROVIDER=gcp" `
  --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE" `
  --set-env-vars "GCP_PROJECT_ID=silicon-guru-472717-q9" `
  --set-env-vars "GEMINI_MODEL=gemini-3-pro-preview" `
  --memory 1Gi `
  --cpu 1 `
  --timeout 300 `
  --max-instances 10
```

**Replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key!**

### 2.3 Get Backend URL

After deployment completes, you'll see:
```
Service URL: https://funlearn-backend-xxxxx-uc.a.run.app
```

**Save this URL!** You'll need it for frontend configuration.

### 2.4 Test Backend

```powershell
# Test health endpoint
curl https://funlearn-backend-xxxxx-uc.a.run.app/health

# Or open in browser:
start https://funlearn-backend-xxxxx-uc.a.run.app/docs
```

---

## Step 3: Prepare Frontend

### 3.1 Create Production Environment File

Create `genlearn-ai/frontend/.env.production`:

```bash
VITE_API_BASE_URL=https://funlearn-backend-xxxxx-uc.a.run.app/api
```

**Replace with your actual Cloud Run URL from Step 2.3!**

### 3.2 Build Frontend

```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\frontend

# Install dependencies (if not already)
npm install

# Build for production
npm run build
```

This creates a `dist` folder with optimized static files.

---

## Step 4: Deploy Frontend to Firebase Hosting

### 4.1 Install Firebase CLI

```powershell
npm install -g firebase-tools
```

### 4.2 Login to Firebase

```powershell
firebase login
```

### 4.3 Initialize Firebase

```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\frontend

# Initialize Firebase Hosting
firebase init hosting
```

**Configuration answers:**:
- Use existing project: **silicon-guru-472717-q9**
- Public directory: **dist**
- Single-page app: **Yes**
- Set up automatic builds: **No**
- Overwrite index.html: **No**

### 4.4 Deploy to Firebase

```powershell
# Deploy
firebase deploy --only hosting
```

You'll get a URL like:
```
Hosting URL: https://silicon-guru-472717-q9.web.app
```

**Save this URL!** This is your public demo link.

---

## Step 5: Update Backend CORS

Now update backend to allow requests from your frontend:

```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\backend

# Redeploy with frontend URL
gcloud run deploy funlearn-backend `
  --source . `
  --region us-central1 `
  --update-env-vars "FRONTEND_URL=https://silicon-guru-472717-q9.web.app"
```

---

## Step 6: Test Full Deployment

1. Open your Firebase URL: `https://silicon-guru-472717-q9.web.app`
2. Try creating an account
3. Test core features
4. Check browser console for errors

---

## Step 7: Monitor and Troubleshoot

### View Backend Logs
```powershell
gcloud run services logs read funlearn-backend --region us-central1 --limit 50
```

### View Firebase Hosting
```powershell
firebase hosting:channel:list
```

### Common Issues

**Issue: CORS Error**
```powershell
# Update CORS by redeploying with correct frontend URL
gcloud run deploy funlearn-backend --update-env-vars "FRONTEND_URL=https://silicon-guru-472717-q9.web.app"
```

**Issue: API Not Found (404)**
- Check VITE_API_BASE_URL in `.env.production`
- Rebuild frontend: `npm run build`
- Redeploy: `firebase deploy --only hosting`

**Issue: Backend Error**
```powershell
# Check logs
gcloud run services logs read funlearn-backend --region us-central1 --limit 100

# Check environment variables
gcloud run services describe funlearn-backend --region us-central1 --format="value(spec.template.spec.containers[0].env)"
```

---

## Cost Breakdown (Free Tier Limits)

### Cloud Run
- **Free tier**: 2M requests/month, 360K GB-seconds CPU, 180K GiB-seconds memory
- **Your usage (estimated)**: 
  - Hackathon demo: ~100-500 requests
  - Scales to zero when idle
  - **Cost: $0**

### Firebase Hosting
- **Free tier**: 10GB storage, 360MB/day transfer
- **Your usage**: 
  - Built app: ~5-10MB
  - Daily transfer: <50MB
  - **Cost: $0**

### Cloud Build (for Cloud Run deployment)
- **Free tier**: 120 build-minutes/day
- **Your usage**: 1-2 builds, ~5 min each
- **Cost: $0**

**Total Monthly Cost: $0** ✅

---

## Updating Your Deployment

### Update Backend
```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\backend
gcloud run deploy funlearn-backend --source . --region us-central1
```

### Update Frontend
```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\frontend
npm run build
firebase deploy --only hosting
```

---

## Alternative: Single Command Deployment Scripts

### Create `deploy-backend.ps1`:

```powershell
# Deploy Backend to Cloud Run
cd D:\Contest\Fun_Learn\genlearn-ai\backend

Write-Host "Deploying backend to Cloud Run..." -ForegroundColor Green

gcloud run deploy funlearn-backend `
  --source . `
  --region us-central1 `
  --platform managed `
  --allow-unauthenticated `
  --port 8080 `
  --memory 1Gi `
  --timeout 300

Write-Host "Backend deployed successfully!" -ForegroundColor Green
Write-Host "Check the Service URL above" -ForegroundColor Yellow
```

### Create `deploy-frontend.ps1`:

```powershell
# Deploy Frontend to Firebase Hosting
cd D:\Contest\Fun_Learn\genlearn-ai\frontend

Write-Host "Building frontend..." -ForegroundColor Green
npm run build

Write-Host "Deploying to Firebase..." -ForegroundColor Green
firebase deploy --only hosting

Write-Host "Frontend deployed successfully!" -ForegroundColor Green
```

---

## Hackathon Submission Links

After deployment, you'll have:

1. **Live Demo**: `https://silicon-guru-472717-q9.web.app`
2. **Backend API**: `https://funlearn-backend-xxxxx-uc.a.run.app`
3. **API Docs**: `https://funlearn-backend-xxxxx-uc.a.run.app/docs`
4. **GitHub Repo**: Your existing repo URL

---

## Quick Reference Commands

```powershell
# View all Cloud Run services
gcloud run services list

# View backend logs (live)
gcloud run services logs tail funlearn-backend --region us-central1

# Delete service (if needed)
gcloud run services delete funlearn-backend --region us-central1

# Check Firebase projects
firebase projects:list

# Check deployed URLs
firebase hosting:sites:list
```

---

## Next Steps for Hackathon

1. ✅ Deploy backend to Cloud Run
2. ✅ Deploy frontend to Firebase Hosting
3. ✅ Test full flow
4. 📹 Record demo video (max 3 minutes)
5. 📝 Update GitHub README with:
   - Live demo link
   - Gemini 3 integration description
   - Setup instructions
6. 📤 Submit to DevPost with:
   - Live demo URL
   - GitHub repo URL
   - Demo video
   - Description (~200 words on Gemini usage)

---

## Support

**GCP Issues**: https://cloud.google.com/support
**Firebase Issues**: https://firebase.google.com/support

**Ready to deploy? Start with Step 2!** 🚀
