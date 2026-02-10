# Update Backend CORS after Frontend Deployment

$FRONTEND_URL = Read-Host "Enter your Firebase Hosting URL (e.g., https://silicon-guru-472717-q9.web.app)"
$PROJECT_ID = "silicon-guru-472717-q9"
$SERVICE_NAME = "funlearn-backend"
$REGION = "us-central1"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Updating Backend CORS Configuration" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Set project
gcloud config set project $PROJECT_ID

# Navigate to backend directory
Set-Location -Path "D:\Contest\Fun_Learn\genlearn-ai\backend"

Write-Host "Updating CORS to allow: $FRONTEND_URL" -ForegroundColor Green
Write-Host ""

gcloud run deploy $SERVICE_NAME `
  --source . `
  --region $REGION `
  --update-env-vars "FRONTEND_URL=$FRONTEND_URL"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "CORS Updated Successfully!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your frontend can now communicate with backend!" -ForegroundColor Yellow
Write-Host "Test your app at: $FRONTEND_URL" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
