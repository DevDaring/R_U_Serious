# Quick Deployment Guide - GCP Only

## 🎯 **Best & Cheapest Option: $0 Cost**

- **Backend**: Cloud Run
- **Frontend**: Firebase Hosting
- **Both on GCP Project**: `silicon-guru-472717-q9`

## ⚠️ **Important: Read This First**

Your app uses CSV files and local media storage. On Cloud Run:
- ✅ **CSV data works** (included in container, resets on restart)
- ✅ **Media generation works** (temporary files, perfect for demo)
- ✅ **No secrets file needed** (Cloud Run handles authentication)
- ✅ **All features work** perfectly for hackathon demo

**Read [CLOUD_RUN_DATA_GUIDE.md](CLOUD_RUN_DATA_GUIDE.md) for details.**

---

## 🚀 **3-Step Deployment**

### **Step 1: Enable APIs & Login**

```powershell
# Login
gcloud auth login

# Set project
gcloud config set project silicon-guru-472717-q9

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login
```

---

### **Step 2: Deploy Backend**

```powershell
# Run the deployment script (recommended)
.\deploy-backend.ps1
```

**You'll be asked for:**
- ✅ **Gemini API Key** (required) - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- ✅ **FIBO API Key** (optional) - For advanced image generation

**What it does:**
- Builds Docker container with CSV data included
- Sets all environment variables securely
- Configures GCP authentication automatically
- Deploys to Cloud Run

**Save the Service URL** (e.g., `https://funlearn-backend-xxxxx-uc.a.run.app`)

**No `.env` file or secret JSON needed!** ✓

---

### **Step 3: Deploy Frontend**

```powershell
# Run the deployment script
.\deploy-frontend.ps1
```

Or manually:
```powershell
cd genlearn-ai\frontend

# Update .env.production with backend URL
# VITE_API_BASE_URL=https://funlearn-backend-xxxxx-uc.a.run.app/api

npm run build
firebase deploy --only hosting
```

**Save the Hosting URL** (e.g., `https://silicon-guru-472717-q9.web.app`)

---

### **Step 4: Update CORS**

```powershell
# Run the script
.\update-backend-cors.ps1
```

---

## ✅ **Done!**

Your app is now live at: `https://silicon-guru-472717-q9.web.app`

**For Hackathon Submission:**
- ✅ Live Demo: Your Firebase URL
- ✅ Backend API: Your Cloud Run URL
- ✅ GitHub Repo: Your existing repo
- 📹 Demo Video: Record 3-minute video
- 📝 Description: ~200 words on Gemini 3 usage

---

## 🔄 **Update Deployment**

**Update Backend:**
```powershell
cd genlearn-ai\backend
gcloud run deploy funlearn-backend --source . --region us-central1
```

**Update Frontend:**
```powershell
cd genlearn-ai\frontend
npm run build
firebase deploy --only hosting
```

---

## 📊 **View Logs**

```powershell
# Backend logs
gcloud run services logs tail funlearn-backend --region us-central1

# View all services
gcloud run services list
```

---

## 💰 **Cost: $0/month**

- Cloud Run: 2M requests/month free
- Firebase Hosting: 10GB storage + 360MB/day transfer free
- Your usage: Well within free tier

---

## 🐛 **Troubleshooting**

**CORS Error?**
```powershell
.\update-backend-cors.ps1
```

**API Not Found?**
- Check `.env.production` has correct backend URL
- Rebuild frontend: `npm run build`
- Redeploy: `firebase deploy --only hosting`

**Backend Error?**
```powershell
gcloud run services logs read funlearn-backend --region us-central1 --limit 50
```

---

## 📚 **Full Documentation**

See [GCP_DEPLOYMENT_STEPS.md](GCP_DEPLOYMENT_STEPS.md) for detailed guide.

---

**Ready? Start with Step 1!** 🎉
