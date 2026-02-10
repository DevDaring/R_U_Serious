# Pre-Flight Deployment Check
# Run this before deploying to verify everything is ready

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Fun Learn - Pre-Deployment Check" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# 1. Check GCP Project
Write-Host "1. Checking GCP Project..." -ForegroundColor Yellow
$project = gcloud config get-value project 2>$null
if ($project -eq "silicon-guru-472717-q9") {
    Write-Host "   [OK] Project: $project" -ForegroundColor Green
} else {
    Write-Host "   [X] Wrong project: $project" -ForegroundColor Red
    Write-Host "   -> Run: gcloud config set project silicon-guru-472717-q9" -ForegroundColor Yellow
    $allPassed = $false
}

# 2. Check gcloud authentication
Write-Host "2. Checking gcloud authentication..." -ForegroundColor Yellow
$auth = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
if ($auth) {
    Write-Host "   [OK] Authenticated as: $auth" -ForegroundColor Green
} else {
    Write-Host "   [X] Not authenticated" -ForegroundColor Red
    Write-Host "   -> Run: gcloud auth login" -ForegroundColor Yellow
    $allPassed = $false
}

# 3. Check gcloud CLI version
Write-Host "3. Checking gcloud CLI..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version 2>$null | Select-String "Google Cloud SDK" | Out-String
    if ($gcloudVersion) {
        Write-Host "   [OK] gcloud CLI installed" -ForegroundColor Green
    }
} catch {
    Write-Host "   [X] gcloud CLI not found" -ForegroundColor Red
    Write-Host "   -> Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    $allPassed = $false
}

# 4. Check Firebase CLI
Write-Host "4. Checking Firebase CLI..." -ForegroundColor Yellow
try {
    $firebaseVersion = firebase --version 2>$null
    if ($firebaseVersion) {
        Write-Host "   [OK] Firebase CLI v$firebaseVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "   [X] Firebase CLI not found" -ForegroundColor Red
    Write-Host "   -> Run: npm install -g firebase-tools" -ForegroundColor Yellow
    $allPassed = $false
}

# 5. Check Node.js (for Firebase)
Write-Host "5. Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "   [OK] Node.js $nodeVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "   [X] Node.js not found" -ForegroundColor Red
    Write-Host "   -> Install from: https://nodejs.org/" -ForegroundColor Yellow
    $allPassed = $false
}

# 6. Check CSV files
Write-Host "6. Checking CSV data files..." -ForegroundColor Yellow
$csvPath = "D:\Contest\Fun_Learn\genlearn-ai\backend\data\csv"
if (Test-Path $csvPath) {
    $csvCount = (Get-ChildItem $csvPath -Filter *.csv).Count
    if ($csvCount -gt 0) {
        Write-Host "   [OK] Found $csvCount CSV files" -ForegroundColor Green
    } else {
        Write-Host "   [X] No CSV files found in $csvPath" -ForegroundColor Red
        $allPassed = $false
    }
} else {
    Write-Host "   [X] CSV directory not found: $csvPath" -ForegroundColor Red
    $allPassed = $false
}

# 7. Check Dockerfile
Write-Host "7. Checking Dockerfile..." -ForegroundColor Yellow
$dockerfilePath = "D:\Contest\Fun_Learn\genlearn-ai\backend\Dockerfile"
if (Test-Path $dockerfilePath) {
    Write-Host "   [OK] Dockerfile exists" -ForegroundColor Green
} else {
    Write-Host "   [X] Dockerfile not found: $dockerfilePath" -ForegroundColor Red
    Write-Host "   -> Deploy scripts should have created this" -ForegroundColor Yellow
    $allPassed = $false
}

# 8. Check deployment scripts
Write-Host "8. Checking deployment scripts..." -ForegroundColor Yellow
$scriptCount = 0
$scripts = @("deploy-backend.ps1", "deploy-frontend.ps1", "update-backend-cors.ps1")
foreach ($script in $scripts) {
    if (Test-Path "D:\Contest\Fun_Learn\$script") {
        $scriptCount++
    }
}
if ($scriptCount -eq 3) {
    Write-Host "   [OK] All deployment scripts found" -ForegroundColor Green
} else {
    Write-Host "   [X] Missing deployment scripts ($scriptCount/3 found)" -ForegroundColor Red
    $allPassed = $false
}

# 9. Check frontend dependencies
Write-Host "9. Checking frontend setup..." -ForegroundColor Yellow
$frontendPath = "D:\Contest\Fun_Learn\genlearn-ai\frontend"
if (Test-Path "$frontendPath\package.json") {
    Write-Host "   [OK] Frontend package.json exists" -ForegroundColor Green
    if (Test-Path "$frontendPath\node_modules") {
        Write-Host "   [OK] Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "   [!] Frontend dependencies not installed" -ForegroundColor Yellow
        Write-Host "   -> Run: cd $frontendPath; npm install" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [X] Frontend package.json not found" -ForegroundColor Red
    $allPassed = $false
}

# 10. Check required GCP APIs
Write-Host "10. Checking GCP APIs..." -ForegroundColor Yellow
$requiredApis = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com"
)
$enabledApis = gcloud services list --enabled --format="value(name)" 2>$null
$missingApis = @()
foreach ($api in $requiredApis) {
    if ($enabledApis -notcontains $api) {
        $missingApis += $api
    }
}
if ($missingApis.Count -eq 0) {
    Write-Host "   [OK] Required APIs enabled" -ForegroundColor Green
} else {
    Write-Host "   [X] Missing APIs: $($missingApis -join ', ')" -ForegroundColor Red
    Write-Host "   -> Run: gcloud services enable $($missingApis -join ' ')" -ForegroundColor Yellow
    $allPassed = $false
}

# Final Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "  ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You're ready to deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Get your Gemini API key: https://makersuite.google.com/app/apikey" -ForegroundColor White
    Write-Host "2. Run: .\deploy-backend.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  SOME CHECKS FAILED" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please fix the issues above before deploying" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host "- Not authenticated: gcloud auth login" -ForegroundColor White
    Write-Host "- Wrong project: gcloud config set project silicon-guru-472717-q9" -ForegroundColor White
    Write-Host "- Missing Firebase: npm install -g firebase-tools" -ForegroundColor White
    Write-Host "- Missing APIs: gcloud services enable run.googleapis.com cloudbuild.googleapis.com" -ForegroundColor White
    Write-Host ""
}
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
