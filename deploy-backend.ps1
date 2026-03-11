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
Write-Host "Enter your Gemini API Key:" -ForegroundColor Yellow
Write-Host "(Get one free at: https://ai.google.dev/)" -ForegroundColor Gray
Write-Host ""

$GEMINI_API_KEY = Read-Host "Gemini API Key (REQUIRED)"
if ([string]::IsNullOrWhiteSpace($GEMINI_API_KEY)) {
    Write-Host "ERROR: Gemini API key is required!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Configuration Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Project: $PROJECT_ID" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White
Write-Host "Service: $SERVICE_NAME" -ForegroundColor White
Write-Host "Gemini 3 API: Configured [OK]" -ForegroundColor Green
Write-Host "Image Provider: Gemini (Imagen 3)" -ForegroundColor Green
Write-Host "Voice Provider: Google Cloud TTS/STT" -ForegroundColor Green
Write-Host ""

# Set project
Write-Host "Setting GCP project..." -ForegroundColor Green
gcloud config set project $PROJECT_ID

# Navigate to backend directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path "$ScriptDir\genlearn-ai\backend"
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

# Ensure data directories exist
Write-Host "Setting up data directories..." -ForegroundColor Green
$DataDirs = @("data/csv", "data/media", "data/mct_images")
foreach ($dir in $DataDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    } else {
        Write-Host "  Verified: $dir" -ForegroundColor Gray
    }
}

# Check if CSV files exist
$CsvCount = (Get-ChildItem -Path "data/csv" -Filter "*.csv" -ErrorAction SilentlyContinue).Count
if ($CsvCount -eq 0) {
    Write-Host "  WARNING: No CSV files found in data/csv/" -ForegroundColor Yellow
    Write-Host "  Creating initial CSV data..." -ForegroundColor Yellow
    
    # Run create_csv_data.py to initialize database
    python create_csv_data.py
    
    if ($LASTEXITCODE -eq 0) {
        $CsvCount = (Get-ChildItem -Path "data/csv" -Filter "*.csv" -ErrorAction SilentlyContinue).Count
        Write-Host "  Created $CsvCount CSV files" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Failed to create CSV files!" -ForegroundColor Red
        Write-Host "  Run 'python create_csv_data.py' manually first" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "  Found $CsvCount CSV files [OK]" -ForegroundColor Green
}

# Enable required GCP APIs
Write-Host ""
Write-Host "Enabling required GCP APIs..." -ForegroundColor Green
$APIs = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "texttospeech.googleapis.com",
    "speech.googleapis.com",
    "aiplatform.googleapis.com"
)
foreach ($api in $APIs) {
    Write-Host "  Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api --project=$PROJECT_ID 2>$null
}
Write-Host "  APIs enabled" -ForegroundColor Green

# Get the project number for Compute Engine default service account
Write-Host ""
Write-Host "Configuring service account permissions..." -ForegroundColor Green
$PROJECT_NUMBER = gcloud projects describe $PROJECT_ID --format="value(projectNumber)" 2>$null
if ([string]::IsNullOrWhiteSpace($PROJECT_NUMBER)) {
    Write-Host "  WARNING: Could not retrieve project number. Skipping IAM setup." -ForegroundColor Yellow
    Write-Host "  Voice features may not work without manual IAM configuration." -ForegroundColor Yellow
} else {
    # Cloud Run uses the Compute Engine default service account
    $ServiceAccount = "$PROJECT_NUMBER-compute@developer.gserviceaccount.com"
    Write-Host "  Service Account: $ServiceAccount" -ForegroundColor Gray

    # Grant necessary IAM permissions for TTS/STT/Imagen
    $Roles = @(
        "roles/aiplatform.user",
        "roles/cloudspeech.client",
        "roles/cloudtts.client"
    )
    foreach ($role in $Roles) {
        Write-Host "  Granting $role..." -ForegroundColor Gray
        gcloud projects add-iam-policy-binding $PROJECT_ID `
            --member="serviceAccount:$ServiceAccount" `
            --role="$role" `
            --condition=None `
            --quiet 2>$null | Out-Null
    }
    Write-Host "  Service account configured" -ForegroundColor Green
}

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

# Deploy to Cloud Run (uses default Compute Engine service account)
Write-Host "Deploying to Cloud Run..." -ForegroundColor Green
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

# Get the service URL
Write-Host ""
Write-Host "Getting service URL..." -ForegroundColor Green
$ServiceUrl = gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Backend Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host ""

# Test the deployment
Write-Host "Testing backend health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ServiceUrl/health" -Method Get -TimeoutSec 10
    if ($response) {
        Write-Host "  ✅ Backend is healthy and responding!" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Backend deployed but health check failed" -ForegroundColor Yellow
    Write-Host "  Give it a minute and check: $ServiceUrl/health" -ForegroundColor Gray
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Save this backend URL:" -ForegroundColor White
Write-Host "   $ServiceUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Test the API (wait 30s for cold start):" -ForegroundColor White
Write-Host "   Health: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "   API Docs: $ServiceUrl/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Deploy frontend:" -ForegroundColor White
Write-Host "   .\deploy-frontend.ps1" -ForegroundColor Cyan
Write-Host "   (You'll need to enter the backend URL above)" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
