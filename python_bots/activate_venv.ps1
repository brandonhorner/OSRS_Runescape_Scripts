# PowerShell script to activate Python virtual environment
Write-Host "Activating Python virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run Python scripts with: python script_name.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available scripts:" -ForegroundColor Cyan
Write-Host "  - area_recorder.py (Screen Area Recorder)" -ForegroundColor White
Write-Host "  - debug_overlay.py (Overlay Debug Tool)" -ForegroundColor White
Write-Host "  - test_overlay.py (Simple Overlay Test)" -ForegroundColor White
Write-Host ""
