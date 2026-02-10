# Deploy Backend to Cloud Run
# Handles all environment variables and service account configuration

$PROJECT_ID = "silicon-guru-472717-q9"
$SERVICE_NAME = "funlearn-backend"
$REGION = "us-central1"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Fun Learn Backend Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Get API keys
Write-Host "Enter your API keys (or press Enter to skip optional ones):" -ForegroundColor Yellow
Write-Host ""

$GEMINI_API_KEY = Read-Host "Gemini API Key (REQUIRED)"
if ([string]::IsNullOrWhiteSpace($GEMINI_API_KEY)) {
    Write-Host "ERROR: Gemini API key is required!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Optional but recommended
$FIBO_API_KEY = Read-Host "FIBO API Key (optional, for advanced image generation)"
if ([string]::IsNullOrWhiteSpace($FIBO_API_KEY)) {
    $FIBO_API_KEY = ""
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Configuration Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Project: $PROJECT_ID" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White
Write-Host "Service: $SERVICE_NAME" -ForegroundColor White
Write-Host "Gemini API: Configured [OK]" -ForegroundColor Green
if ($FIBO_API_KEY) { Write-Host "FIBO API: Configured [OK]" -ForegroundColor Green }
Write-Host ""

# Set project
Write-Host "Setting GCP project..." -ForegroundColor Green
gcloud config set project $PROJECT_ID

# Navigate to backend directory
Set-Location -Path "D:\Contest\Fun_Learn\genlearn-ai\backend"

Write-Host ""
Write-Host "Building and deploying to Cloud Run..." -ForegroundColor Green
Write-Host "This may take 5-8 minutes..." -ForegroundColor Yellow
Write-Host ""

# Build environment variables string
$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "Generated SECRET_KEY for production" -ForegroundColor Green

$ENV_VARS = "APP_ENV=production," +
    "DEBUG=false," +
    "SECRET_KEY=$SECRET_KEY," +
    "BACKEND_PORT=8080," +
    "AI_PROVIDER=gemini," +
    "IMAGE_PROVIDER=gemini," +
    "VOICE_TTS_PROVIDER=gcp," +
    "VOICE_STT_PROVIDER=gcp," +
    "GEMINI_API_KEY=$GEMINI_API_KEY," +
    "GCP_PROJECT_ID=$PROJECT_ID," +
    "GEMINI_MODEL=gemini-3-pro-preview," +
    "GEMINI_IMAGE_MODEL=gemini-3-pro-image-preview," +
    "APP_API_KEY=kd_dreaming007"

if ($FIBO_API_KEY) {
    $ENV_VARS += ",FIBO_API_KEY=$FIBO_API_KEY"
}

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME `
  --source . `
  --region $REGION `
  --platform managed `
  --allow-unauthenticated `
  --port 8080 `
  --set-env-vars $ENV_VARS `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --max-instances 10 `
  --min-instances 0 `
  --cpu-boost

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Deployment failed! Check the error above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Backend Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Copy the Service URL from above" -ForegroundColor White
Write-Host "   Example: https://funlearn-backend-xxxxx-uc.a.run.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Test the backend:" -ForegroundColor White
Write-Host "   Health: https://[YOUR-URL]/health" -ForegroundColor Cyan
Write-Host "   API Docs: https://[YOUR-URL]/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Run: .\deploy-frontend.ps1 (and enter the backend URL)" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
