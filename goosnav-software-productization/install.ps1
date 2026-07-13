param(
    [ValidateSet("User", "Repo")]
    [string]$Scope = "User",
    [string]$RepoPath = ""
)

$ErrorActionPreference = "Stop"
$SkillName = "goosnav-software-productization"
$SourceDir = [System.IO.Path]::GetFullPath((Split-Path -Parent $MyInvocation.MyCommand.Path))

function Copy-Skill([string]$DestinationRoot) {
    $Destination = Join-Path $DestinationRoot $SkillName
    New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null
    $ResolvedDestination = [System.IO.Path]::GetFullPath($Destination)
    if ($ResolvedDestination -eq $SourceDir) {
        Write-Host "Already canonical: $Destination"
        return
    }
    $StagingRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    $StagingSkill = Join-Path $StagingRoot $SkillName
    New-Item -ItemType Directory -Force -Path $StagingRoot | Out-Null
    Copy-Item -Recurse -Force $SourceDir $StagingSkill
    if (Test-Path $Destination) { Remove-Item -Recurse -Force $Destination }
    Move-Item $StagingSkill $Destination
    Remove-Item -Recurse -Force $StagingRoot
    Write-Host "Installed: $Destination"
}

function Remove-Legacy([string]$DestinationRoot) {
    $Destination = Join-Path $DestinationRoot $SkillName
    if (-not (Test-Path $Destination)) { return }
    $ResolvedDestination = [System.IO.Path]::GetFullPath($Destination)
    if ($ResolvedDestination -eq $SourceDir) {
        Write-Host "Legacy source copy retained while installer is running: $Destination"
        return
    }
    Remove-Item -Recurse -Force $Destination
    Write-Host "Removed duplicate: $Destination"
}

if ($Scope -eq "User") {
    $Root = Join-Path $HOME ".agents\skills"
    Copy-Skill $Root
    Remove-Legacy (Join-Path $HOME ".codex\skills")
    Remove-Legacy (Join-Path $HOME ".claude\skills")
    Write-Host "Canonical Agent Skill: $(Join-Path $Root $SkillName)"
} else {
    if ([string]::IsNullOrWhiteSpace($RepoPath)) { throw "-RepoPath is required when -Scope Repo" }
    $Resolved = (Resolve-Path $RepoPath).Path
    $Root = Join-Path $Resolved ".agents\skills"
    Copy-Skill $Root
    Remove-Legacy (Join-Path $Resolved ".codex\skills")
    Remove-Legacy (Join-Path $Resolved ".claude\skills")
    Write-Host "Canonical repository skill: $(Join-Path $Root $SkillName)"
}
