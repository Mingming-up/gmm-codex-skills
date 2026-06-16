param(
    [int]$Port = 0,
    [int[]]$CandidatePorts = @(6528, 7890, 7897, 1080, 10808, 10809, 20171, 2080),
    [switch]$DetectOnly
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function Test-HttpConnectProxy {
    param([int]$PortToTest)

    $proxy = "http://127.0.0.1:$PortToTest"
    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & curl.exe -I -x $proxy "https://api.openai.com" --connect-timeout 10 --ssl-no-revoke 2>&1
    }
    finally {
        $ErrorActionPreference = $oldErrorActionPreference
    }
    $text = ($output | Out-String)
    return $text -match "HTTP/1\.1 200 Connection established"
}

function Test-TcpListening {
    param([int]$PortToTest)

    $lines = & netstat -ano 2>$null
    return ($lines | Select-String -SimpleMatch ":$PortToTest ").Count -gt 0
}

if ($Port -eq 0) {
    foreach ($candidate in $CandidatePorts) {
        if ((Test-TcpListening -PortToTest $candidate) -and (Test-HttpConnectProxy -PortToTest $candidate)) {
            $Port = $candidate
            break
        }
    }
}

if ($Port -eq 0) {
    throw "No working HTTP CONNECT proxy was found. Start the proxy app or pass -Port with the app's HTTP proxy port."
}

$proxy = "http://127.0.0.1:$Port"
$noProxy = "localhost,127.0.0.1,::1"

Write-Host "Using proxy: $proxy"

if ($DetectOnly) {
    exit 0
}

$codexDir = Join-Path $env:USERPROFILE ".codex"
$envPath = Join-Path $codexDir "1.env"

if (-not (Test-Path -LiteralPath $codexDir)) {
    New-Item -ItemType Directory -Path $codexDir -Force | Out-Null
}

if (Test-Path -LiteralPath $envPath) {
    Copy-Item -LiteralPath $envPath -Destination "$envPath.bak" -Force
}

$content = @(
    "HTTP_PROXY=$proxy"
    "HTTPS_PROXY=$proxy"
    "ALL_PROXY=$proxy"
    "NO_PROXY=$noProxy"
    "http_proxy=$proxy"
    "https_proxy=$proxy"
    "all_proxy=$proxy"
    "no_proxy=$noProxy"
)

Set-Content -LiteralPath $envPath -Value $content -Encoding ASCII

$pairs = @(
    @("HTTP_PROXY", $proxy),
    @("HTTPS_PROXY", $proxy),
    @("ALL_PROXY", $proxy),
    @("NO_PROXY", $noProxy),
    @("http_proxy", $proxy),
    @("https_proxy", $proxy),
    @("all_proxy", $proxy),
    @("no_proxy", $noProxy)
)

foreach ($pair in $pairs) {
    $name = $pair[0]
    $value = $pair[1]
    [Environment]::SetEnvironmentVariable($name, $value, "User")
    & setx.exe $name $value | Out-Null
    Set-Item -Path "Env:$name" -Value $value
}

Write-Host ""
Write-Host "Wrote Codex proxy record: $envPath"
Write-Host "Wrote Windows user environment variables under HKCU\Environment."
Write-Host ""
Write-Host "Verify with:"
Write-Host "  reg query HKCU\Environment /v HTTP_PROXY"
Write-Host ""
Write-Host "Then fully quit Codex and reopen it. Restart Windows if Codex was already running."
