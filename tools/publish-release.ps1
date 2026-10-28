param(
  [Parameter(Mandatory=$true)][string]$Tag,
  [string]$Notes = 'BETA_RELEASE_NOTES.md'
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$Zip = Join-Path $Root ("artifacts\E2FSPROGS-$Tag-win64.zip")
$NotesFile = Join-Path $Root $Notes
if (-not (Test-Path -LiteralPath $Zip)) { throw "Missing ZIP: $Zip" }
if (-not (Test-Path -LiteralPath $NotesFile)) { throw "Missing release notes: $NotesFile" }
$env:GCM_INTERACTIVE = 'never'
$env:GIT_TERMINAL_PROMPT = '0'
$credentialLines = @('protocol=https','host=github.com','') | git credential fill
$passwordLine = $credentialLines | Where-Object { $_ -match '^password=' } | Select-Object -First 1
if (-not $passwordLine) { throw 'GitHub credential unavailable' }
$headers = @{
  Authorization = "Bearer $($passwordLine.Substring(9))"
  Accept = 'application/vnd.github+json'
  'User-Agent' = 'E2FSPROGS-Release-Publisher'
  'X-GitHub-Api-Version' = '2022-11-28'
}
$base = 'https://api.github.com/repos/rokkystudio/E2FSPROGS/releases'
$release = $null
try { $release = Invoke-RestMethod -Method Get -Uri "$base/tags/$Tag" -Headers $headers } catch {
  if ([int]$_.Exception.Response.StatusCode -ne 404) { throw }
}
if (-not $release) {
  $payload = @{
    tag_name = $Tag
    target_commitish = 'main'
    name = "E2FSPROGS $Tag - Windows x64"
    body = [IO.File]::ReadAllText($NotesFile)
    draft = $false
    prerelease = $true
  } | ConvertTo-Json -Depth 4
  $release = Invoke-RestMethod -Method Post -Uri $base -Headers $headers -ContentType 'application/json' -Body ([Text.Encoding]::UTF8.GetBytes($payload))
}
if (@($release.assets | Where-Object { $_.name -eq (Split-Path -Leaf $Zip) }).Count -eq 0) {
  $upload = $release.upload_url.Split('{')[0] + '?name=' + [uri]::EscapeDataString((Split-Path -Leaf $Zip))
  $asset = Invoke-RestMethod -Method Post -Uri $upload -Headers $headers -ContentType 'application/octet-stream' -InFile $Zip
  Write-Output "Asset: $($asset.browser_download_url)"
}
Write-Output "Release: $($release.html_url)"
