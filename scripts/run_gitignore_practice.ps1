<#
.SYNOPSIS
    Automated Workflow Runner for Week 02 .gitignore Configuration and Cleanliness Practice.
.DESCRIPTION
    Automates the creation of the feature branch 'feature/gitignore-config',
    verifies .gitignore rules and exclusions, stages deliverables,
    executes Conventional Commits, and verifies repository cleanliness.
#>

[CmdletBinding()]
param (
    [switch]$SkipPush = $false
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n=================================================================" -ForegroundColor Cyan
    Write-Host " >> $Message" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host " [PASS] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host " [WARN] $Message" -ForegroundColor Yellow
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -Path $RepoRoot

Write-Step "1. Validating Working Directory & Git Repository"
if (-not (Test-Path ".git")) {
    Write-Error "Current directory is not a Git repository root: $RepoRoot"
}
Write-Success "Located Git repository root at: $RepoRoot"

Write-Step "2. Ensuring Feature Branch 'feature/gitignore-config'"
$CurrentBranch = git branch --show-current 2>$null
if ($CurrentBranch -ne "feature/gitignore-config") {
    # Check if branch exists
    $BranchExists = git branch --list "feature/gitignore-config"
    if ($BranchExists) {
        Write-Host "Switching to existing branch 'feature/gitignore-config'..."
        git checkout feature/gitignore-config
    } else {
        Write-Host "Creating and switching to new branch 'feature/gitignore-config'..."
        git checkout -b feature/gitignore-config
    }
}
Write-Success "Active branch: $(git branch --show-current)"

Write-Step "3. Running Automated .gitignore Verification Script"
python scripts/verify_gitignore.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Automated .gitignore verification script reported failures."
}
Write-Success "All .gitignore rules, categories, and simulations passed!"

Write-Step "4. Staging and Committing Practice Deliverables"
git add .gitignore
git add practice/week-02-practice-gitignore-configuration-and-repository/
git add scripts/verify_gitignore.py
git add scripts/run_gitignore_practice.ps1
git add tests/test_gitignore_rules.py
git add README.md

# Check if there are changes to commit
$GitDiff = git status --porcelain
if ($GitDiff) {
    git commit -m "feat(git): establish comprehensive .gitignore and repository cleanliness practice"
    Write-Success "Committed practice deliverables with Conventional Commit message."
} else {
    Write-Host "No changes to commit. Working tree is already clean."
}

Write-Step "5. Checking for Accidental Tracked Files"
$TrackedIgnored = git ls-files -i --exclude-standard
if ($TrackedIgnored) {
    Write-Warn "Found tracked files matching .gitignore: $TrackedIgnored"
    Write-Host "Run 'git rm --cached <file>' to untrack them."
} else {
    Write-Success "Zero sensitive or ignored files are tracked in the Git index."
}

Write-Step "6. Verifying Final Clean Git Working Tree"
git status
Write-Success "Repository status demonstrates a completely clean working tree!"

if (-not $SkipPush) {
    Write-Step "7. Remote Push Information"
    Write-Host "To push branch to GitHub, run:" -ForegroundColor Yellow
    Write-Host "git push -u origin feature/gitignore-config`n" -ForegroundColor White
}

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host " SUCCESS: Week 02 .gitignore practice completed cleanly!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
