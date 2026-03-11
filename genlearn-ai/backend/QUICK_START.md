# R U Serious? Backend - Quick Start Guide

Get the R U Serious? backend up and running in minutes!

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Installation Steps

### Step 1: Navigate to Backend Directory

```bash
cd D:\Contest\GenAI_Learn\genlearn-ai\backend
```

### Step 2: Verify Installation

Run the verification script to check all files are in place:

```bash
python verify_installation.py
```

This will check:
- ✓ All route files
- ✓ Configuration files
- ✓ Directory structure
- ✓ Python version
- ✓ Installed dependencies

### Step 3: Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Unix/Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pandas - CSV handling
- Pydantic - Data validation
- httpx - Async HTTP client
- Passlib - Password hashing
- python-jose - JWT tokens
- And more...

### Step 5: Configure Environment

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# Unix/Linux/macOS
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Minimum required configuration
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key

# Optional providers
FIBO_API_KEY=your_fibo_key
GCP_TTS_API_KEY=your_gcp_key
# ... etc
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 6: Start the Server

**Option A - Quick Start Scripts:**

**Windows:**
```bash
start.bat
```

**Unix/Linux/macOS:**
```bash
./start.sh
```

**Option B - Python Runner (Recommended for Development):**
```bash
python run.py --reload
```

**Option C - Direct Uvicorn:**
```bash
uvicorn app.main:app --reload --port 8000
```

### Step 7: Verify Server is Running

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Testing the API

### 1. Test Login (Get JWT Token)

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin\", \"password\": \"password123\"}"
```

**Using PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/auth/login `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username": "admin", "password": "password123"}'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": "USR001",
    "username": "admin",
    "role": "admin"
  }
}
```

### 2. Test Authenticated Endpoint

Copy the `access_token` from the login response and use it:

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Use Interactive Documentation

The easiest way to test is using Swagger UI:
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your JWT token
4. Test any endpoint interactively

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `password123`

**Test User Account:**
- Username: `DebK`
- Password: `password123`

> ⚠️ **Important:** Change these passwords before deploying to production!

## Common Issues & Solutions

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use a different port
python run.py --port 8001

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Unix/Linux/macOS:
lsof -ti:8000 | xargs kill -9
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Provider Connection Errors

**Error:** `GEMINI_API_KEY not set`

**Solution:**
- Check `.env` file exists
- Verify API key is set correctly
- No quotes around the key value
- No spaces before/after `=`

### Database/CSV Errors

**Error:** `File not found: users.csv`

**Solution:**
```bash
# Ensure data directory structure exists
python verify_installation.py

# CSV files should be in: data/csv/
# Check if CSV files exist, if not, they'll be created on first run
```

## Development Workflow

### 1. Make Code Changes

Edit files in `app/` directory:
- Routes: `app/api/routes/`
- Models: `app/models/`
- Services: `app/services/`
- Config: `app/config.py`

### 2. Auto-Reload

If you started with `--reload` flag, the server automatically restarts when you save changes.

### 3. Test Changes

Use Swagger UI to test your changes immediately:
http://localhost:8000/docs

### 4. Check Logs

Server logs appear in the terminal. Look for:
- Request logs
- Error messages
- Provider status

## Project Structure Reference

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── dependencies.py  # Auth & shared deps
│   │   └── routes/          # API endpoints (12 files)
│   ├── services/            # Business logic
│   ├── database/            # CSV handlers
│   ├── models/              # Pydantic models
│   └── utils/               # Helper functions
├── data/
│   ├── csv/                 # Database files
│   └── media/               # Generated media
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .env                    # Your config (create this!)
├── run.py                  # Server runner
├── start.bat               # Windows quick start
├── start.sh                # Unix quick start
└── verify_installation.py  # Installation check
```

## Next Steps

1. **Explore API Documentation**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Understand request/response formats

2. **Configure Providers**
   - Add API keys for AI providers (Gemini, OpenAI, etc.)
   - Add image generation keys (FIBO, Stability)
   - Add voice service keys (GCP TTS/STT)

3. **Test Core Features**
   - Authentication flow
   - Create learning session
   - Generate content
   - Test quiz functionality

4. **Connect Frontend**
   - Update frontend API base URL
   - Test CORS configuration
   - Verify token handling

5. **Review Documentation**
   - `README.md` - Complete guide
   - `API_DOCUMENTATION.md` - Detailed API reference
   - `IMPLEMENTATION_SUMMARY.md` - Technical overview

## Production Deployment

When ready for production:

1. **Security**
   - Change all default passwords
   - Use strong SECRET_KEY
   - Set `DEBUG=false`
   - Enable HTTPS

2. **Configuration**
   - Set `APP_ENV=production`
   - Configure proper CORS origins
   - Set up monitoring

3. **Deployment Options**
   - Docker container
   - Cloud platform (AWS, Azure, GCP)
   - VPS with systemd service
   - Kubernetes cluster

## Support & Resources

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Main Spec**: `../genlearn-ai-prompt.md`
- **Technical Details**: `IMPLEMENTATION_SUMMARY.md`

## Troubleshooting Checklist

Before asking for help, verify:
- [ ] Python 3.11+ installed: `python --version`
- [ ] Dependencies installed: `pip list`
- [ ] .env file exists and configured
- [ ] Verification script passes: `python verify_installation.py`
- [ ] Port 8000 is available
- [ ] Virtual environment activated (if using)
- [ ] No firewall blocking port 8000

## Success Indicators

Your backend is working correctly when:
- ✓ Server starts without errors
- ✓ http://localhost:8000/health returns "healthy"
- ✓ http://localhost:8000/docs loads successfully
- ✓ Login returns JWT token
- ✓ Authenticated endpoints work with token

---

**Ready to code?** Start the server and visit http://localhost:8000/docs!
