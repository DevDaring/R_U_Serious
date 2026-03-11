# Deploy Frontend to Firebase Hosting

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Fun Learn Frontend Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path "$ScriptDir\genlearn-ai\frontend"
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Node modules not found. Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install dependencies!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Dependencies installed" -ForegroundColor Green
    Write-Host ""
}

# Check Firebase configuration
if (-not (Test-Path "firebase.json")) {
    Write-Host "ERROR: firebase.json not found!" -ForegroundColor Red
    Write-Host "Run 'firebase init' first to set up Firebase Hosting" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$BACKEND_URL = Read-Host "Enter your Cloud Run backend URL (e.g., https://funlearn-backend-xxxxx-uc.a.run.app)"

if ([string]::IsNullOrWhiteSpace($BACKEND_URL)) {
    Write-Host "ERROR: Backend URL is required!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Remove trailing slash if present
$BACKEND_URL = $BACKEND_URL.TrimEnd('/')

# Create .env.production file
Write-Host "Creating production environment file..." -ForegroundColor Green
$envContent = "VITE_API_BASE_URL=$BACKEND_URL/api"
Set-Content -Path ".env.production" -Value $envContent

Write-Host "Environment configured with backend: $BACKEND_URL/api" -ForegroundColor Green
Write-Host ""

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Green
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed! Please fix errors and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Deploying to Firebase Hosting..." -ForegroundColor Green
firebase deploy --only hosting

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Deployment failed! Check the error above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Not logged in to Firebase: Run 'firebase login'" -ForegroundColor White
    Write-Host "  - Wrong project: Run 'firebase use --add'" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

# Get hosting URL
Write-Host ""
Write-Host "Getting hosting URL..." -ForegroundColor Green
$ProjectId = (Get-Content "firebase.json" | ConvertFrom-Json).hosting.site
if (-not $ProjectId) {
    $ProjectId = (Get-Content ".firebaserc" -ErrorAction SilentlyContinue | ConvertFrom-Json).projects.default
}

$HostingUrl = "https://$ProjectId.web.app"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Frontend Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend URL: $HostingUrl" -ForegroundColor Cyan
Write-Host "Backend URL:  $BACKEND_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Your Fun Learn app is now LIVE!" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Test your application:" -ForegroundColor White
Write-Host "   $HostingUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Create a test account and verify:" -ForegroundColor White
Write-Host "   • User registration works" -ForegroundColor Gray
Write-Host "   • Gemini 3 text generation works" -ForegroundColor Gray
Write-Host "   • Imagen 3 image generation works" -ForegroundColor Gray
Write-Host "   • Voice synthesis works (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Record demo video for hackathon" -ForegroundColor White
Write-Host ""
Write-Host "4. Submit to Gemini 3 Hackathon:" -ForegroundColor White
Write-Host "   https://gemini3.devpost.com/" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
