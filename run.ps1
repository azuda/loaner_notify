# run.ps1 - Windows wrapper for loaner_notify
# Creates the venv on first run, then runs run.py.

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

  & $venvPython run.py
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
