# Background Remover - Context Menu Fix (PowerShell with elevation)
Write-Host "Background Remover - Context Menu Fix" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Check if running as administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  Not running as Administrator. Requesting elevation..." -ForegroundColor Yellow
    Write-Host ""

    # Get the current script path and arguments
    $scriptPath = $MyInvocation.MyCommand.Path
    $pythonScript = Join-Path $PSScriptRoot "fix_context_menu.py"

    # Create a new PowerShell process with elevation
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "powershell"
    $startInfo.Arguments = "-Command `"cd '$($PWD.Path)'; python '$pythonScript'; Write-Host ''; Write-Host 'Press any key to continue...'; `$null = `$Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')`""
    $startInfo.UseShellExecute = $true
    $startInfo.Verb = "runas"
    $startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal

    try {
        [System.Diagnostics.Process]::Start($startInfo)
        Write-Host "✅ Administrator window opened. Check the new window for results." -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to elevate privileges: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Please run this script manually as Administrator." -ForegroundColor Yellow
    }
}
else {
    Write-Host "✅ Running as Administrator" -ForegroundColor Green
    Write-Host ""

    # Run the Python script directly
    $pythonScript = Join-Path $PSScriptRoot "fix_context_menu.py"
    python $pythonScript

    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
