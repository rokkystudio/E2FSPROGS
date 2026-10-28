$ErrorActionPreference='Stop'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
$env:GCM_INTERACTIVE='never';$env:GIT_TERMINAL_PROMPT='0'
$credentialLines=@('protocol=https','host=github.com','') | git credential fill
$pwLine=$credentialLines | Where-Object { $_ -match '^password=' } | Select-Object -First 1
if(-not $pwLine){throw 'Git credential unavailable'}
$token=$pwLine.Substring(9)
$headers=@{'Authorization'="Bearer $token";'Accept'='application/vnd.github+json';'User-Agent'='E2FSPROGS-ReleasePublisher';'X-GitHub-Api-Version'='2022-11-28'}
$repo='rokkystudio/E2FSPROGS'
$tag='v0.1.0-alpha.1'
$api="https://api.github.com/repos/$repo/releases"
$release=$null
try {$release=Invoke-RestMethod -Method Get -Uri "$api/tags/$tag" -Headers $headers} catch { if([int]$_.Exception.Response.StatusCode -ne 404){throw} }
if(-not $release){
 $body=@{tag_name=$tag;target_commitish='main';name='E2FSPROGS v0.1.0-alpha.1 — Windows x64 preview';body=[IO.File]::ReadAllText('C:\FILES\PROJECTS\E2FSPROGS\RELEASE_NOTES.md');draft=$false;prerelease=$true;generate_release_notes=$false} | ConvertTo-Json -Depth 4
 $release=Invoke-RestMethod -Method Post -Uri $api -Headers $headers -ContentType 'application/json' -Body ([Text.Encoding]::UTF8.GetBytes($body))
}
Write-Output "Release available: $($release.html_url)"
$file=Get-Item 'C:\FILES\PROJECTS\E2FSPROGS\artifacts\E2FSPROGS-v0.1.0-alpha.1-win64.zip'
if(@($release.assets | Where-Object {$_.name -eq $file.Name}).Count -eq 0){
 $uploadUri=$release.upload_url.Split('{')[0]+'?name='+[uri]::EscapeDataString($file.Name)
 $asset=Invoke-RestMethod -Method Post -Uri $uploadUri -Headers $headers -ContentType 'application/octet-stream' -InFile $file.FullName
 Write-Output "Asset uploaded: $($asset.browser_download_url) ($($asset.size) bytes)"
}else {Write-Output 'Asset already exists'}
