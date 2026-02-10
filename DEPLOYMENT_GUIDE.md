# Deployment Guide for Gemini 3 Hackathon

## Current Deployment Plan

- **Backend**: GCP Cloud Run (Project: `silicon-guru-472717-q9`)
- **Frontend**: Web hosting platform (Firebase/Vercel/Netlify)

## Required Configuration Changes

### 1. Backend Configuration

#### Update CORS for Production
File: `genlearn-ai/backend/app/main.py`

Add your production frontend URL to allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-frontend-domain.web.app",  # Firebase
        "https://your-app.vercel.app",            # Vercel
        # Add your actual frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Environment Variables for Cloud Run
Create `.env.production` file:
```bash
# App Settings
APP_ENV=production
DEBUG=false
SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
FRONTEND_URL=https://your-frontend-domain.web.app

# Gemini API (Required for hackathon)
GEMINI_API_KEY=<your-gemini-api-key>
GEMINI_MODEL=gemini-3-pro-preview
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002

# GCP
GCP_PROJECT_ID=silicon-guru-472717-q9
GCP_STT_API_KEY=<your-key>
GCP_TTS_API_KEY=<your-key>

# Providers
AI_PROVIDER=gemini
IMAGE_PROVIDER=gemini
VOICE_TTS_PROVIDER=gcp
VOICE_STT_PROVIDER=gcp
```

#### Dockerfile for Cloud Run
Create `genlearn-ai/backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/csv data/media

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 2. Frontend Configuration

#### Environment Variables for Production
Create `.env.production`:
```bash
VITE_API_BASE_URL=https://your-backend-abc123.run.app/api
```

Replace with your actual Cloud Run URL after deployment.

### 3. Deployment Steps

#### Backend Deployment (Cloud Run)

1. **Build and deploy to Cloud Run**:
```bash
cd genlearn-ai/backend

# Build and deploy
gcloud run deploy funlearn-backend \
  --source . \
  --project silicon-guru-472717-q9 \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=production \
  --set-env-vars GEMINI_API_KEY=<your-key> \
  --set-env-vars GCP_PROJECT_ID=silicon-guru-472717-q9 \
  --port 8080
```

2. **Note the deployed URL** (e.g., `https://funlearn-backend-abc123-uc.a.run.app`)

#### Frontend Deployment Options

##### Option A: Firebase Hosting (Recommended - Google Ecosystem)

```bash
cd genlearn-ai/frontend

# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase
firebase init hosting

# Select project: silicon-guru-472717-q9

# Set build directory: dist
# Single-page app: Yes
# Set up automatic builds: No

# Update .env.production with backend URL
echo "VITE_API_BASE_URL=https://your-backend-url.run.app/api" > .env.production

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

##### Option B: Vercel

```bash
cd genlearn-ai/frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# During setup, add environment variable:
# VITE_API_BASE_URL = https://your-backend-url.run.app/api
```

##### Option C: Netlify

```bash
cd genlearn-ai/frontend

# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=dist

# Set environment variable in Netlify dashboard:
# VITE_API_BASE_URL = https://your-backend-url.run.app/api
```

### 4. Final CORS Update

After deploying frontend, update backend CORS:

**Option 1: Via Cloud Run Console**
- Go to Cloud Run service
- Edit & Deploy New Revision
- Add environment variable: `FRONTEND_URL=https://your-frontend-url`

**Option 2: Redeploy with updated env**
```bash
gcloud run deploy funlearn-backend \
  --source . \
  --project silicon-guru-472717-q9 \
  --region us-central1 \
  --set-env-vars FRONTEND_URL=https://your-frontend-url \
  --update-env-vars
```

### 5. Testing the Deployment

1. Visit your frontend URL
2. Try logging in
3. Test core features
4. Check browser console for CORS errors
5. Verify API calls in Network tab

### 6. Hackathon Submission Requirements

For Gemini 3 Hackathon, you need:

✅ **Public Project Link**: Your frontend URL (e.g., `https://funlearn.web.app`)
✅ **Public GitHub Repository**: Required for custom apps
✅ **Demo Video**: ~3 minutes showing Gemini integration
✅ **Description**: ~200 words on Gemini 3 features used

## Important Notes

### Static Files & Media
Your backend serves static files from `/media` and `/data` directories. Ensure:
- Cloud Run has persistent storage OR
- Use Cloud Storage for media files
- Update code to serve from Cloud Storage URLs

### Cost Considerations
- **Cloud Run**: Free tier includes 2M requests/month
- **Firebase Hosting**: 10GB storage, 360MB/day transfer on free tier
- **Vercel/Netlify**: Free tier sufficient for demo

### Security
- Use environment variables for all secrets
- Never commit API keys to GitHub
- Enable Cloud Run authentication if needed

## Common Issues

### CORS Errors
- Ensure FRONTEND_URL is set correctly in backend
- Check browser console for exact error
- Verify Cloud Run allows your frontend origin

### API Connection Failed
- Check VITE_API_BASE_URL is correct
- Ensure Cloud Run service is publicly accessible
- Test backend health endpoint: `https://your-backend.run.app/health`

### Media Files Not Loading
- Check Cloud Run logs
- Verify media directory exists
- Consider using Cloud Storage for production

## Alternative: Demo-Only Deployment

If full deployment is complex, you can:
1. Deploy backend only to Cloud Run
2. Run frontend locally but point to production backend
3. Record demo video
4. Submit GitHub repo with instructions

Judges can run frontend locally with your deployed backend URL.

---

## Hackathon Submission Checklist

- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to hosting platform
- [ ] Both URLs tested and working
- [ ] GitHub repository is public
- [ ] README.md updated with:
  - [ ] Project description
  - [ ] Gemini 3 integration details
  - [ ] Setup instructions
  - [ ] Live demo links
- [ ] Demo video recorded (max 3 minutes)
- [ ] Submission includes:
  - [ ] Working demo link
  - [ ] GitHub repo URL
  - [ ] Demo video
  - [ ] Description of Gemini features

Good luck with the Gemini 3 Hackathon! 🚀
