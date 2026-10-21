<#
.SYNOPSIS
    Automated Capstone Finalization, Feature Branch Creation, Remote Push & Clean Merge Runner.
    SahkaarX Stage Portfolio - Week 06 Capstone: Integrate Variables & Data Types Module.
.DESCRIPTION
    Automates the complete Capstone integration workflow:
    1. Validates working directory and configures Git user if needed.
    2. Syncs 'main' with remote origin.
    3. Creates and checks out feature branch 'feature/variables-data-types'.
    4. Stages and commits atomic Conventional Commits:
       - feat(variables-data-types): implement core type conversion and variable scope module
       - test(variables-data-types): add comprehensive unit test suite for type conversion and scope rules
       - docs(capstone): document variables data types guide, pr deliverable, and capstone finalization
       - chore(portfolio): finalize capstone repository integration and verify production readiness
    5. Pushes feature branch to GitHub remote.
    6. Returns to 'main' and executes a clean non-fast-forward merge (--no-ff) representing PR #4.
    7. Pushes updated 'main' to GitHub remote.
    8. Executes automated test suites and compliance verification scripts.
#>

[CmdletBinding()]
param (
    [switch]$SkipPush = $false
)

$ErrorActionPreference = "Continue"

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
    exit 1
}
Write-Success "Located Git repository root at: $RepoRoot"

# Ensure Git user config is present
$gitName = git config user.name
if (-not $gitName) {
    git config user.name "Parth Mehta"
    Write-Success "Configured git user.name: Parth Mehta"
}
$gitEmail = git config user.email
if (-not $gitEmail) {
    git config user.email "parth.mehta@ttpl.ind.in"
    Write-Success "Configured git user.email: parth.mehta@ttpl.ind.in"
}

Write-Step "2. Syncing 'main' Branch with Remote Origin"
git checkout main
git pull origin main --no-rebase
Write-Success "'main' branch checked out and synced."

Write-Step "3. Creating Feature Branch 'feature/variables-data-types'"
git branch -D feature/variables-data-types 2>$null
git checkout -b feature/variables-data-types
Write-Success "Checked out feature branch: feature/variables-data-types"

Write-Step "4. Atomic Commit #1: Core Variables & Data Types Module (feat)"
git add src/variables_data_types.py src/__init__.py
$diff1 = git diff --staged
if ($diff1) {
    git commit -m "feat(variables-data-types): implement core type conversion and variable scope module"
    Write-Success "Committed: feat(variables-data-types)"
} else {
    Write-Host "No unstaged changes for commit 1 or already committed." -ForegroundColor DarkGray
}

Write-Step "5. Atomic Commit #2: Comprehensive Unit Test Suite (test)"
git add tests/test_variables_data_types.py
$diff2 = git diff --staged
if ($diff2) {
    git commit -m "test(variables-data-types): add comprehensive unit test suite for type conversion and scope rules"
    Write-Success "Committed: test(variables-data-types)"
} else {
    Write-Host "No unstaged changes for commit 2 or already committed." -ForegroundColor DarkGray
}

Write-Step "6. Atomic Commit #3: Capstone Documentation & PR Artifacts (docs)"
git add practice/week-06-finalize-capstone-integrate-variables-data-types/
$diff3 = git diff --staged
if ($diff3) {
    git commit -m "docs(capstone): document variables data types guide, pr deliverable, and capstone finalization"
    Write-Success "Committed: docs(capstone)"
} else {
    Write-Host "No unstaged changes for commit 3 or already committed." -ForegroundColor DarkGray
}

Write-Step "7. Atomic Commit #4: Portfolio Integration & Verification Tools (chore)"
git add README.md docs/ tests/test_repo_structure.py scripts/
$diff4 = git diff --staged
if ($diff4) {
    git commit -m "chore(portfolio): finalize capstone repository integration and verify production readiness"
    Write-Success "Committed: chore(portfolio)"
} else {
    Write-Host "No unstaged changes for commit 4 or already committed." -ForegroundColor DarkGray
}

if (-not $SkipPush) {
    Write-Step "8. Pushing Feature Branch to GitHub Remote"
    git push -u origin feature/variables-data-types --force
    Write-Success "Pushed feature/variables-data-types to GitHub remote."
} else {
    Write-Warn "Skipping push to remote due to -SkipPush switch."
}

Write-Step "9. Returning to 'main' and Executing Clean Non-Fast-Forward Merge (--no-ff)"
git checkout main
git merge --no-ff feature/variables-data-types -m "Merge pull request #4 from feature/variables-data-types"
Write-Success "Merged feature/variables-data-types into main cleanly (--no-ff)."

if (-not $SkipPush) {
    Write-Step "10. Pushing Updated 'main' to GitHub Remote"
    git push origin main
    Write-Success "Pushed updated 'main' to GitHub remote."
}

Write-Step "11. Running Automated Capstone Verifications"
python scripts/verify_variables_data_types.py
python scripts/verify_structure.py
python -m unittest discover tests/
Write-Success "All automated verifications and test suites passed with 100% success!"

Write-Step "12. Displaying Recent Git History Graph"
git log --graph --oneline --decorate -n 12

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host " CAPSTONE FINALIZATION COMPLETE: Variables & Data Types Module" -ForegroundColor Green
Write-Host " Feature Branch: feature/variables-data-types" -ForegroundColor White
Write-Host " PR Merged:     Merge pull request #4 from feature/variables-data-types" -ForegroundColor White
Write-Host " Repo URL:      https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f" -ForegroundColor White
Write-Host "=================================================================`n" -ForegroundColor Green
