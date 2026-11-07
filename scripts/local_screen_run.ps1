# Start local llama-server (Vulkan), run screening evaluation, then stop the server.
# Usage (repo root):  powershell -ExecutionPolicy Bypass -File scripts\local_screen_run.ps1
param([string[]]$Sets = @('dev','heldout'), [int]$Limit = 0, [string]$Prompt = 'screen-v1')
$ErrorActionPreference = 'Stop'
$log = "outputs\local-review-screening\server.log"
$srv = Start-Process llama-server -PassThru -WindowStyle Minimized -RedirectStandardError $log -ArgumentList @(
  '-m','outputs\local-review-feasibility\models\Qwen3-14B-Q5_K_M.gguf','--device','Vulkan0','-ngl','all',
  '-c','16384','-np','1','--host','127.0.0.1','--port','18080','--reasoning','off','-fa','auto')
try {
  for ($i = 0; $i -lt 120; $i++) {
    try { if ((Invoke-WebRequest -UseBasicParsing http://127.0.0.1:18080/health -TimeoutSec 2).StatusCode -eq 200) { break } } catch {}
    Start-Sleep 2
  }
  $ErrorActionPreference = 'Continue'
  $env:PYTHONIOENCODING = 'utf-8'
  $extra = @(); if ($Limit -gt 0) { $extra = @('--limit', $Limit) }
  foreach ($Set in $Sets) {
    python scripts\local_screen.py eval --set $Set --prompt $Prompt @extra 2>&1 | Tee-Object "outputs\local-review-screening\run-$Set-$Prompt.log"
  }
} finally {
  Stop-Process -Id $srv.Id -Force
  Write-Host "llama-server stopped"
}
