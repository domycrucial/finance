<#
.SYNOPSIS
Installs the Enterprise React UI/UX Skills Library into Google Antigravity.
.PARAMETER Scope
'Workspace' installs to .\.agents\skills\ (current project).
'Global' installs to $env:USERPROFILE\.gemini\config\skills\ (all projects).
#>
param(
    [ValidateSet("Workspace", "Global")]
    [string]$Scope = "Workspace",
    [string]$WorkspacePath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$SourceSkills = Join-Path $PSScriptRoot ".agents\skills"

if ($Scope -eq "Workspace") {
    $TargetDir = Join-Path $WorkspacePath ".agents\skills"
} else {
    $TargetDir = Join-Path $env:USERPROFILE ".gemini\config\skills"
}

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Get-ChildItem -Path $SourceSkills -Directory | ForEach-Object {
    $Dest = Join-Path $TargetDir $_.Name
    if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
    Copy-Item -Recurse -Force $_.FullName $Dest
    Write-Host "Installed skill: $($_.Name) -> $Dest" -ForegroundColor Green
}

Write-Host "`nDone! Run 'python scripts/validate-skills.py "$TargetDir"' to verify." -ForegroundColor Cyan
