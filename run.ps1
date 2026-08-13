# run.ps1 - Windows wrapper for loaner_notify
# Creates the venv on first run, sets the CA bundle if cert.pem exists, then runs run.py.

$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
  $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

  if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
      py -3 -m venv .venv
    }
    else {
      python -m venv .venv
    }
    if (-not (Test-Path $venvPython)) {
      throw "Failed to create .venv - is Python 3 installed and on PATH?"
    }
    & $venvPython -m pip install --quiet -r requirements.txt
  }

  # use cloudflare gateway root cert
  $certPath = Join-Path $PSScriptRoot "cert.pem"
  if (Test-Path $certPath) {
    $env:REQUESTS_CA_BUNDLE = $certPath
    $env:CF_CA_BUNDLE = $certPath
    $env:SSL_CERT_FILE = $certPath
    $env:CURL_CA_BUNDLE = $certPath
    Write-Host "Using CA bundle at $certPath for SSL verification"
  }
  else {
    Write-Host "Warning: CA bundle not found at $certPath - SSL verification may fail"
  }

  & $venvPython run.py
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
