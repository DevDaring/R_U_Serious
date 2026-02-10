# Pre-Deployment Checklist

Run this checklist before deploying to ensure everything is ready.

## ✅ Prerequisites Check

### 1. GCP Project ✓
```powershell
# Check current project
gcloud config get-value project

# Should show: silicon-guru-472717-q9
# If not, set it:
gcloud config set project silicon-guru-472717-q9
```

**Expected:** `silicon-guru-472717-q9`

---

### 2. gcloud CLI Installed ✓
```powershell
gcloud --version
```

**Expected:** 
```
Google Cloud SDK 450.0.0+
```

**If not installed:** https://cloud.google.com/sdk/docs/install

---

### 3. gcloud Authentication ✓
```powershell
gcloud auth list
```

**Expected:** See your Google account marked as ACTIVE

**If not logged in:**
```powershell
gcloud auth login
```

---

### 4. Firebase CLI Installed ✓
```powershell
firebase --version
```

**Expected:** `13.0.0` or higher

**If not installed:**
```powershell
npm install -g firebase-tools
```

---

### 5. Firebase Authentication ✓
```powershell
firebase projects:list
```

**Expected:** See `silicon-guru-472717-q9` in the list

**If not logged in:**
```powershell
firebase login
```

---

### 6. Gemini API Key Ready ✓

**Get your key:** https://makersuite.google.com/app/apikey

**Test it:**
```powershell
curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY"
```

**Expected:** JSON response with list of models

**Keep this key handy** - you'll need it during deployment!

---

### 7. CSV Data Present ✓
```powershell
Get-ChildItem D:\Contest\Fun_Learn\genlearn-ai\backend\data\csv
```

**Expected:** See 18 CSV files including:
- users.csv
- sessions.csv
- avatars.csv
- characters.csv
- feynman_sessions.csv
- etc.

---

### 8. Backend Dockerfile Exists ✓
```powershell
Test-Path D:\Contest\Fun_Learn\genlearn-ai\backend\Dockerfile
```

**Expected:** `True`

---

### 9. Frontend Package Ready ✓
```powershell
cd D:\Contest\Fun_Learn\genlearn-ai\frontend
npm install
```

**Expected:** Dependencies installed successfully

---

### 10. Required GCP APIs Enabled ✓
```powershell
gcloud services list --enabled --filter="name:(run.googleapis.com OR cloudbuild.googleapis.com)"
```

**If not enabled:**
```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable speech.googleapis.com
```

---

## 🎯 Final Pre-Flight Check

Run this command to verify everything:

```powershell
# Check all at once
Write-Host "Checking GCP Project..." -ForegroundColor Cyan
$project = gcloud config get-value project
Write-Host "Project: $project" -ForegroundColor $(if ($project -eq "silicon-guru-472717-q9") {"Green"} else {"Red"})

Write-Host "`nChecking gcloud auth..." -ForegroundColor Cyan
$auth = gcloud auth list --filter=status:ACTIVE --format="value(account)"
Write-Host "Authenticated: $auth" -ForegroundColor $(if ($auth) {"Green"} else {"Red"})

Write-Host "`nChecking Firebase..." -ForegroundColor Cyan
try {
    firebase --version | Out-Null
    Write-Host "Firebase CLI: Installed ✓" -ForegroundColor Green
} catch {
    Write-Host "Firebase CLI: Not installed ✗" -ForegroundColor Red
}

Write-Host "`nChecking CSV files..." -ForegroundColor Cyan
$csvCount = (Get-ChildItem D:\Contest\Fun_Learn\genlearn-ai\backend\data\csv *.csv).Count
Write-Host "CSV files: $csvCount" -ForegroundColor $(if ($csvCount -gt 0) {"Green"} else {"Red"})

Write-Host "`nChecking Dockerfile..." -ForegroundColor Cyan
$dockerfileExists = Test-Path D:\Contest\Fun_Learn\genlearn-ai\backend\Dockerfile
Write-Host "Dockerfile: $(if ($dockerfileExists) {'Found ✓'} else {'Missing ✗'})" -ForegroundColor $(if ($dockerfileExists) {"Green"} else {"Red"})

Write-Host "`n" -NoNewline
Write-Host "================================" -ForegroundColor Cyan
if ($project -eq "silicon-guru-472717-q9" -and $auth -and $dockerfileExists -and $csvCount -gt 0) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "You're ready to deploy!" -ForegroundColor Green
} else {
    Write-Host "⚠️ SOME CHECKS FAILED" -ForegroundColor Yellow
    Write-Host "Fix the issues above before deploying" -ForegroundColor Yellow
}
Write-Host "================================" -ForegroundColor Cyan
```

**Save this as:** `pre-flight-check.ps1`

---

## 📝 Information to Gather

Before starting deployment, have these ready:

### Required:
- [x] **Gemini API Key** - https://makersuite.google.com/app/apikey
  - Format: `AIzaSy...` (39 characters)
  - Keep it secure, don't share publicly

### Optional:
- [ ] **FIBO API Key** - For advanced image generation
  - Can skip if not needed
  - Press Enter when prompted

---

## 🚀 Ready to Deploy?

### If all checks pass ✅

**Run in this order:**

```powershell
# 1. Backend deployment (5-8 minutes)
.\deploy-backend.ps1

# Copy the backend URL, then:

# 2. Frontend deployment (3-5 minutes)
.\deploy-frontend.ps1

# Copy the frontend URL, then:

# 3. CORS update (1-2 minutes)
.\update-backend-cors.ps1
```

### If checks fail ❌

**Common fixes:**

**gcloud not installed:**
```powershell
# Download and install
https://cloud.google.com/sdk/docs/install
```

**Wrong project:**
```powershell
gcloud config set project silicon-guru-472717-q9
```

**Not authenticated:**
```powershell
gcloud auth login
firebase login
```

**Missing CSV files:**
- Check if you're in the right directory
- Verify `data/csv/` folder exists in backend

**Missing Dockerfile:**
- Verify deployment scripts created it
- Check `genlearn-ai/backend/Dockerfile` exists

---

## 📊 Expected Timeline

| Step | Time | Action |
|------|------|--------|
| Pre-flight check | 2 min | Run checklist |
| Backend build | 5 min | Cloud Build creates container |
| Backend deploy | 3 min | Deploy to Cloud Run |
| Frontend build | 2 min | npm run build |
| Frontend deploy | 2 min | Firebase upload |
| CORS update | 1 min | Redeploy backend |
| **Total** | **~15 min** | **Complete deployment** |

---

## 🆘 Need Help?

### Check logs:
```powershell
# Cloud Run logs
gcloud run services logs tail funlearn-backend --region us-central1

# Cloud Build logs
gcloud builds list --limit 5
```

### Test connectivity:
```powershell
# Test backend health
curl https://your-backend-url.run.app/health

# Test frontend
curl https://your-frontend-url.web.app
```

### Common issues:
- **"Project not found"** → Run `gcloud config set project silicon-guru-472717-q9`
- **"Permission denied"** → Run `gcloud auth login`
- **"API not enabled"** → Run `gcloud services enable run.googleapis.com`

---

## ✅ Final Checklist Before Starting

- [ ] All prerequisites checked
- [ ] Gemini API key ready
- [ ] In correct directory: `D:\Contest\Fun_Learn`
- [ ] Terminal open in PowerShell
- [ ] Deployment scripts present (deploy-backend.ps1, etc.)
- [ ] 15 minutes of uninterrupted time
- [ ] Notepad ready to save URLs

**All good? Let's deploy!** 🚀

```powershell
.\deploy-backend.ps1
```
