# Deploy Frontend to Firebase Hosting

$BACKEND_URL = Read-Host "Enter your Cloud Run backend URL (e.g., https://funlearn-backend-xxxxx-uc.a.run.app)"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Deploying Fun Learn Frontend" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location -Path "D:\Contest\Fun_Learn\genlearn-ai\frontend"

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

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Frontend Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your app is now live!" -ForegroundColor Yellow
Write-Host "Check the Hosting URL above" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update backend CORS with your frontend URL" -ForegroundColor White
Write-Host "2. Test your live application" -ForegroundColor White
Write-Host "3. Record demo video for hackathon" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
