param(
    [ValidateSet("User", "Repo")]
    [string]$Scope = "User",
    [string]$RepoPath = ""
)

$ErrorActionPreference = "Stop"
$PackRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $MyInvocation.MyCommand.Path))

if ($Scope -eq "Repo") {
    if ([string]::IsNullOrWhiteSpace($RepoPath) -or -not (Test-Path -LiteralPath $RepoPath -PathType Container)) {
        throw "-RepoPath must name an existing repository directory when -Scope Repo"
    }
    $ResolvedRepo = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $RepoPath).Path)
    if ($ResolvedRepo -eq [System.IO.Path]::GetPathRoot($ResolvedRepo)) {
        throw "Refusing to install into a filesystem root"
    }
}

$Installers = @(Get-ChildItem -LiteralPath $PackRoot -Directory | ForEach-Object {
    $ShellInstaller = Join-Path $_.FullName "install.sh"
    if (Test-Path -LiteralPath $ShellInstaller -PathType Leaf) {
        $Candidate = Join-Path $_.FullName "install.ps1"
        if (-not (Test-Path -LiteralPath $Candidate -PathType Leaf)) { throw "Missing PowerShell installer beside $ShellInstaller" }
        Get-Item -LiteralPath $Candidate
    }
} | Sort-Object FullName)

if ($Installers.Count -eq 0) { throw "No primary skill directories containing install.ps1 were found" }

foreach ($Installer in $Installers) {
    $SkillDir = [System.IO.Path]::GetFullPath($Installer.Directory.FullName)
    $SkillName = Split-Path -Leaf $SkillDir
    if ($Scope -eq "Repo") {
        $Destination = [System.IO.Path]::GetFullPath((Join-Path $ResolvedRepo ".agents\skills\$SkillName"))
        $Prefix = $SkillDir.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
        if ($Destination -eq $SkillDir -or $Destination.StartsWith($Prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to treat source skill as its installed destination: $SkillName"
        }
    }
    Write-Host "Installing $SkillName"
    if ($Scope -eq "User") {
        & $Installer.FullName -Scope User
    } else {
        & $Installer.FullName -Scope Repo -RepoPath $ResolvedRepo
    }
}

Write-Host "Installed $($Installers.Count) primary Goosnav skills. Supplemental skills under extra-skills are opt-in."
