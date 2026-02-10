# Cloud Run Deployment - Data Persistence & Secrets Guide

## Understanding Cloud Run Storage

### ⚠️ What Cloud Run Does NOT Persist

Cloud Run is **stateless** and **ephemeral**:
- File system is **read-only except /tmp**
- Any file changes are **lost** when container restarts
- Containers can restart at any time
- Each request may hit a different container instance

---

## 📁 CSV Files (User Data)

### Current Setup
Your app uses CSV files for data storage:
```
data/csv/
├── users.csv
├── sessions.csv
├── avatars.csv
├── characters.csv
├── feynman_sessions.csv
├── learning_history.csv
└── ... (18 files total)
```

### ✅ Solution for Hackathon Demo

**Approach**: Include initial CSV data in Docker image

**What this means:**
- ✅ Read operations work perfectly
- ✅ Users can test all features
- ⚠️ New users/data are lost on restart
- ⚠️ Perfect for demo, NOT for production

**Implementation:**
```dockerfile
# Dockerfile includes CSV files
COPY data/csv/ ./data/csv/
```

### 🎯 Behavior During Hackathon

1. **User creates account** → Works! Saved to CSV
2. **User takes quiz** → Works! Score saved
3. **Container restarts** → All new data lost, resets to initial state
4. **For your demo** → Record before restart! ✓

### 🚀 For Production (Future)

Replace CSV with:
- **Cloud SQL** (PostgreSQL/MySQL)
- **Firestore** (NoSQL, better for prototypes)
- **Cloud Storage** (for large files)

---

## 🖼️ Media Files (Images/Audio/Video)

### Current Setup
Generated media stored in:
```
data/media/
├── avatars/
├── characters/
├── generated_images/
├── generated_videos/
├── audio/
└── uploads/
```

### ✅ Solution for Hackathon Demo

**Approach**: Use ephemeral storage (temporary)

**What this means:**
- ✅ Generation works during session
- ✅ Users can download immediately
- ⚠️ Files deleted on container restart
- ⚠️ Each container has its own storage

**Implementation:**
```dockerfile
# Create directories at runtime
RUN mkdir -p data/media/avatars \
    data/media/generated_images \
    ...
```

### 🎯 Behavior During Hackathon

1. **Generate avatar** → Works! File created
2. **View/download avatar** → Works! File accessible
3. **Container restarts** → File gone
4. **Different container** → File not there

**Best Practice for Demo:**
- Generate media during your demo session
- Download important files immediately
- Don't rely on old media files

### 🚀 For Production (Future)

Use **Cloud Storage**:
```python
from google.cloud import storage

# Upload to Cloud Storage instead of local disk
client = storage.Client()
bucket = client.bucket('funlearn-media')
blob = bucket.blob(f'avatars/{user_id}.png')
blob.upload_from_file(file)
```

---

## 🔐 Secret JSON File (Service Account)

### Current Setup
Your `.env` references:
```bash
GOOGLE_APPLICATION_CREDENTIALS="./secrets/gen-lang-client-0511107229-995568b40390.json"
```

### ❌ Problem
- **Security risk** to include in Docker image
- **Bad practice** to commit secrets to container
- **Not necessary** on Cloud Run

### ✅ Solution: Use Cloud Run Default Service Account

Cloud Run automatically provides authentication!

**Your code already handles this:**
```python
# app/services/voice_providers/gcp_tts.py
if credentials_path and os.path.exists(credentials_path):
    # Use service account file
    self.credentials = service_account.Credentials.from_service_account_file(...)
else:
    # Fall back to Application Default Credentials ← THIS!
    self.credentials, project = default(scopes=CLOUD_TTS_SCOPES)
```

**What happens on Cloud Run:**
1. No `GOOGLE_APPLICATION_CREDENTIALS` set → Falls back to default
2. Cloud Run provides credentials automatically
3. Your code works without the JSON file! ✓

### 🎯 Configuration

**In deploy-backend.ps1:**
- ✅ Don't set `GOOGLE_APPLICATION_CREDENTIALS`
- ✅ Set `GCP_PROJECT_ID` only
- ✅ Cloud Run handles authentication

**No changes needed to your code!** It already supports this.

---

## 🔑 Environment Variables (.env file)

### Current .env File
```bash
GEMINI_API_KEY="AIzaSy..."
GCP_PROJECT_ID="gen-lang-client-0511107229"
FIBO_API_KEY="a2e0b4a3..."
GOOGLE_APPLICATION_CREDENTIALS="./secrets/..."  # ← NOT NEEDED
```

### ✅ Solution: Cloud Run Environment Variables

**Set via deployment script:**
```powershell
gcloud run deploy funlearn-backend `
  --set-env-vars "GEMINI_API_KEY=AIzaSy...,GCP_PROJECT_ID=silicon-guru-472717-q9,..."
```

**Security:**
- ✅ API keys stored securely in Cloud Run
- ✅ Not visible in Docker image
- ✅ Not in source code
- ✅ Encrypted at rest

### 🎯 What Gets Set

Our deployment script sets:
```
APP_ENV=production
DEBUG=false
BACKEND_PORT=8080
AI_PROVIDER=gemini
IMAGE_PROVIDER=gemini
VOICE_TTS_PROVIDER=gcp
VOICE_STT_PROVIDER=gcp
GEMINI_API_KEY=<your-key>
GCP_PROJECT_ID=silicon-guru-472717-q9
GEMINI_MODEL=gemini-3-pro-preview
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002
APP_API_KEY=kd_dreaming007
FIBO_API_KEY=<optional>
```

**Note:** `.env` file is **NOT** copied to Docker (excluded in `.dockerignore`)

---

## 🔒 Secrets Best Practices

### For Hackathon (Current Setup) ✅

**Acceptable:**
- Set env vars via `--set-env-vars`
- Use Cloud Run's built-in encryption
- API keys only visible to your project

### For Production (Future) 🚀

Use **Secret Manager**:
```powershell
# Store secret
echo -n "AIzaSy..." | gcloud secrets create gemini-api-key --data-file=-

# Mount in Cloud Run
gcloud run deploy funlearn-backend `
  --set-secrets="GEMINI_API_KEY=gemini-api-key:latest"
```

Benefits:
- ✅ Centralized secret management
- ✅ Audit logs
- ✅ Automatic rotation
- ✅ Fine-grained access control

---

## 📋 Deployment Checklist

### Before Deployment

- [x] CSV files in `data/csv/` (will be included)
- [x] `.dockerignore` excludes `.env` and secrets
- [x] Dockerfile copies CSV but not media
- [x] Have your Gemini API key ready

### During Deployment

Run: `.\deploy-backend.ps1`

**It will ask for:**
1. ✅ Gemini API Key (required)
2. ✅ FIBO API Key (optional)

**It will automatically:**
- Set all environment variables
- Configure providers
- Enable Cloud Run authentication
- Deploy with proper settings

### After Deployment

- [x] Test health endpoint: `https://[URL]/health`
- [x] Test API docs: `https://[URL]/docs`
- [x] Try creating a user (will work!)
- [x] Generate media (will work during session!)

---

## 🧪 Testing Data Persistence

### Test 1: CSV Data (Initial State)

```powershell
# Check initial users
curl https://[YOUR-URL]/api/users

# Create new user
curl -X POST https://[YOUR-URL]/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{"username":"test","email":"test@test.com","password":"password"}'

# New user exists ✓
curl https://[YOUR-URL]/api/users

# Force container restart (or wait for auto-scaling)
gcloud run services update funlearn-backend --region us-central1

# New user is gone (reset to initial CSV data)
curl https://[YOUR-URL]/api/users
```

### Test 2: Media Files

```powershell
# Generate avatar
curl -X POST https://[YOUR-URL]/api/avatar/generate

# Download works ✓
curl https://[YOUR-URL]/media/avatars/[id].png

# After restart - file is gone
```

---

## ✅ What Works for Hackathon

### Perfectly Fine ✓
- Read existing data from CSV
- Create users/sessions during demo
- Generate images/audio during demo
- Download generated files immediately
- All Gemini API features
- All GCP voice features

### Limitations (Acceptable for Demo) ⚠️
- Data resets on container restart
- Media files are temporary
- No cross-container file sharing

### Not Needed 🚫
- Service account JSON file
- .env file in Docker
- Persistent storage setup

---

## 🎬 Demo Strategy

**Best Approach:**

1. **Deploy** → Use scripts to deploy
2. **Test immediately** → Create demo users, generate content
3. **Record video** → Capture working demo
4. **For judges** → They'll test on fresh instance (works fine!)

**Timeline:**
- Container stays warm for ~15 minutes of inactivity
- Your demo session = continuous activity = same container
- Perfect for recording! ✓

---

## 🚨 Common Issues & Solutions

### "User not found after creation"
**Cause:** Multiple containers, user created in different instance
**Solution:** Set `--min-instances 1` (already in script) ✓

### "Media file not accessible"
**Cause:** File created in different container
**Solution:** Download files immediately after generation

### "GCP authentication failed"
**Cause:** Service account permissions
**Solution:** Cloud Run automatically has permissions for same project ✓

### "CSV file not found"
**Cause:** Not copied to Docker
**Solution:** Check Dockerfile has `COPY data/csv/ ./data/csv/` ✓

---

## 💰 Cost Impact

**Good news:** Ephemeral storage is **FREE**

- No Cloud Storage costs
- No Cloud SQL costs
- Only Cloud Run compute (free tier covers hackathon)

**Estimated hackathon cost: $0** ✅

---

## 🎯 Summary

| Component | Solution | Demo Impact |
|-----------|----------|-------------|
| **CSV Data** | Included in image | ✅ Works, resets on restart |
| **Media Files** | Ephemeral storage | ✅ Works during session |
| **Service Account** | Default credentials | ✅ Automatic, no JSON needed |
| **API Keys** | Environment variables | ✅ Secure, properly configured |
| **Persistence** | Not required | ✅ Perfect for demo |

**Ready to deploy? Run `.\deploy-backend.ps1`!** 🚀
