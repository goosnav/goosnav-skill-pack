param(
    [ValidateSet("User", "Repo")]
    [string]$Scope = "User",
    [string]$RepoPath = ""
)

$ErrorActionPreference = "Stop"
$SkillName = "goosnav-software-productization"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Copy-Skill([string]$DestinationRoot) {
    $Destination = Join-Path $DestinationRoot $SkillName
    New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null
    $ResolvedDestination = [System.IO.Path]::GetFullPath($Destination)
    $ResolvedSource = [System.IO.Path]::GetFullPath($SourceDir)
    if ($ResolvedDestination -eq $ResolvedSource) {
        Write-Host "Already installed: $Destination"
        return
    }
    $StagingRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    $StagingSkill = Join-Path $StagingRoot $SkillName
    New-Item -ItemType Directory -Force -Path $StagingRoot | Out-Null
    Copy-Item -Recurse -Force $SourceDir $StagingSkill
    if (Test-Path $Destination) {
        Remove-Item -Recurse -Force $Destination
    }
    Move-Item $StagingSkill $Destination
    Remove-Item -Recurse -Force $StagingRoot
    Write-Host "Installed: $Destination"
}

if ($Scope -eq "User") {
    Copy-Skill (Join-Path $HOME ".claude\skills")
    Copy-Skill (Join-Path $HOME ".codex\skills")
    Copy-Skill (Join-Path $HOME ".agents\skills")
    Write-Host "Claude Code: /$SkillName"
    Write-Host "Codex:       `$$SkillName"
} else {
    if ([string]::IsNullOrWhiteSpace($RepoPath)) {
        throw "-RepoPath is required when -Scope Repo"
    }
    $Resolved = (Resolve-Path $RepoPath).Path
    Copy-Skill (Join-Path $Resolved ".claude\skills")
    Copy-Skill (Join-Path $Resolved ".codex\skills")
    Copy-Skill (Join-Path $Resolved ".agents\skills")
    Write-Host "Installed repository-scoped copies in: $Resolved"
}
