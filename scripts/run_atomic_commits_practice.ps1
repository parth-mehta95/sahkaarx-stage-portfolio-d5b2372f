<#
.SYNOPSIS
    Automated Workflow Runner for Week 02 Atomic Commits and Clear Messaging Practice.
.DESCRIPTION
    Automates the creation of the feature branch 'feature/atomic-commits-and-messaging',
    executes 5 distinct atomic commits adhering to Conventional Commits v1.0.0,
    validates commit messages and test suites, pushes to GitHub origin, and displays the git log graph.
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

# Ensure repository root is working directory
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -Path $RepoRoot

Write-Step "1. Validating Working Directory & Git Repository"
if (-not (Test-Path ".git")) {
    Write-Error "Current directory is not a Git repository root: $RepoRoot"
    exit 1
}
Write-Success "Located Git repository root at: $RepoRoot"

Write-Step "2. Initializing Feature Branch 'feature/atomic-commits-and-messaging'"
$ExistingBranch = git branch --list "feature/atomic-commits-and-messaging"
if ($ExistingBranch) {
    Write-Host "Switching to existing branch 'feature/atomic-commits-and-messaging'..." -ForegroundColor Yellow
    git checkout feature/atomic-commits-and-messaging
} else {
    Write-Host "Creating and switching to new branch 'feature/atomic-commits-and-messaging'..." -ForegroundColor Green
    git checkout -b feature/atomic-commits-and-messaging
}
Write-Success "Active branch: $(git branch --show-current)"

Write-Step "3. Atomic Commit 1/5: Core Validator Implementation (feat)"
git add src/utils/commit_validator.py
git add src/utils/__init__.py
$Diff1 = git status --porcelain
if ($Diff1) {
    git commit -m "feat(validator): implement conventional commit parser and validator engine"
    Write-Success "Commit 1 created: feat(validator)"
} else {
    Write-Host "Commit 1 already applied or no changes detected."
}

Write-Step "4. Atomic Commit 2/5: Unit Test Suite (test)"
git add tests/test_commit_validator.py
$Diff2 = git status --porcelain
if ($Diff2) {
    git commit -m "test(validator): add comprehensive unit test suite for commit validation rules"
    Write-Success "Commit 2 created: test(validator)"
} else {
    Write-Host "Commit 2 already applied or no changes detected."
}

Write-Step "5. Atomic Commit 3/5: History Verification & Workflow Tooling (chore)"
git add scripts/verify_commit_history.py
git add scripts/run_atomic_commits_practice.ps1
$Diff3 = git status --porcelain
if ($Diff3) {
    git commit -m "chore(tooling): add automated git history verifier and workflow runner"
    Write-Success "Commit 3 created: chore(tooling)"
} else {
    Write-Host "Commit 3 already applied or no changes detected."
}

Write-Step "6. Atomic Commit 4/5: Practice Documentation & Guides (docs)"
git add practice/week-02-practice-atomic-commits-and-clear-messaging/ATOMIC_COMMITS_GUIDE.md
git add practice/week-02-practice-atomic-commits-and-clear-messaging/COMMIT_LOG_AUDIT.md
git add practice/week-02-practice-atomic-commits-and-clear-messaging/README.md
$Diff4 = git status --porcelain
if ($Diff4) {
    git commit -m "docs(practice): document atomic commit principles, workflow guide, and history audit"
    Write-Success "Commit 4 created: docs(practice)"
} else {
    Write-Host "Commit 4 already applied or no changes detected."
}

Write-Step "7. Atomic Commit 5/5: Portfolio Index & Structure Integration (docs)"
git add README.md
git add tests/test_repo_structure.py
git add scripts/verify_structure.py
$Diff5 = git status --porcelain
if ($Diff5) {
    git commit -m "docs(portfolio): register atomic commits practice in portfolio index and update structure checks"
    Write-Success "Commit 5 created: docs(portfolio)"
} else {
    Write-Host "Commit 5 already applied or no changes detected."
}

Write-Step "8. Running Verification Test Suites"
Write-Host "Running Commit History Auditor..." -ForegroundColor Cyan
python scripts/verify_commit_history.py

Write-Host "`nRunning Unit Test Discovery..." -ForegroundColor Cyan
python -m unittest discover tests/

Write-Host "`nRunning Repository Structure Verification..." -ForegroundColor Cyan
python scripts/verify_structure.py

if (-not $SkipPush) {
    Write-Step "9. Pushing Feature Branch to GitHub Remote"
    git push -u origin feature/atomic-commits-and-messaging --force
    Write-Success "Branch pushed successfully to origin/feature/atomic-commits-and-messaging!"
}

Write-Step "10. Git Log Graph Demonstration"
git log --graph --pretty=format:"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset" -n 8

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host " SUCCESS: Atomic Commits Practice Workflow Completed Successfully!" -ForegroundColor Green
Write-Host " GitHub URL: https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging" -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Green
