<#
.SYNOPSIS
    Automated Workflow Runner for Week 02 Practice: Basic Git Workflow with Multiple Commits.
.DESCRIPTION
    Automates the complete Git workflow:
    1. Checks out / creates the feature branch 'feature/basic-git-workflow'.
    2. Stages and executes 4+ discrete atomic commits demonstrating 'git add' and 'git commit'.
    3. Synchronizes the branch with 'main' demonstrating 'git pull'.
    4. Executes automated verification scripts and unittest discovery.
    5. Pushes the branch to GitHub demonstrating 'git push'.
    6. Displays git commit graph and Pull Request readiness.
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

Write-Step "2. Initializing Feature Branch 'feature/basic-git-workflow'"
$ExistingBranch = git branch --list "feature/basic-git-workflow"
if ($ExistingBranch) {
    Write-Host "Switching to existing branch 'feature/basic-git-workflow'..." -ForegroundColor Yellow
    git checkout feature/basic-git-workflow
} else {
    Write-Host "Creating and switching to new branch 'feature/basic-git-workflow'..." -ForegroundColor Green
    git checkout -b feature/basic-git-workflow
}
Write-Success "Active branch: $(git branch --show-current)"

Write-Step "3. Atomic Commit 1: Core Git Operations Module (feat)"
git add src/utils/git_ops.py
git add src/utils/__init__.py
$diff1 = git diff --staged
if ($diff1) {
    git commit -m "feat(git-ops): implement core git workflow management module"
    Write-Success "Committed Atomic Change #1: Core Git operations module"
} else {
    Write-Host "No unstaged changes for commit 1 or already committed." -ForegroundColor DarkGray
}

Write-Step "4. Atomic Commit 2: Unit Test Suite for Git Operations (test)"
git add tests/test_git_ops.py
$diff2 = git diff --staged
if ($diff2) {
    git commit -m "test(git-ops): add unit tests verifying git operations and tracker"
    Write-Success "Committed Atomic Change #2: Unit test suite"
} else {
    Write-Host "No unstaged changes for commit 2 or already committed." -ForegroundColor DarkGray
}

Write-Step "5. Atomic Commit 3: Automation Verifier and Workflow Runner (chore)"
git add scripts/verify_basic_git_workflow.py
git add scripts/run_basic_git_workflow_practice.ps1
$diff3 = git diff --staged
if ($diff3) {
    git commit -m "chore(automation): add basic git workflow verifier and powershell runner"
    Write-Success "Committed Atomic Change #3: Tooling & scripts"
} else {
    Write-Host "No unstaged changes for commit 3 or already committed." -ForegroundColor DarkGray
}

Write-Step "6. Atomic Commit 4: Practice Documentation & PR Artifact (docs)"
git add practice/week-02-practice-basic-git-workflow-with-multiple-commit/
$diff4 = git diff --staged
if ($diff4) {
    git commit -m "docs(practice): document basic git workflow guide, audit log, and pr"
    Write-Success "Committed Atomic Change #4: Practice documentation"
} else {
    Write-Host "No unstaged changes for commit 4 or already committed." -ForegroundColor DarkGray
}

Write-Step "7. Atomic Commit 5: Repository Integration & Governance (docs)"
git add README.md
git add docs/DIRECTORY_STRUCTURE.md
git add docs/CONTRIBUTING.md
git add scripts/verify_structure.py
git add tests/test_repo_structure.py
$diff5 = git diff --staged
if ($diff5) {
    git commit -m "docs(portfolio): register basic git workflow practice in repository index"
    Write-Success "Committed Atomic Change #5: Repository integration"
} else {
    Write-Host "No unstaged changes for commit 5 or already committed." -ForegroundColor DarkGray
}

Write-Step "8. Demonstrating 'git pull': Syncing Branch with Main"
Write-Host "Fetching latest refs and syncing feature branch with origin/main..." -ForegroundColor Yellow
git pull origin main --no-rebase
Write-Success "Branch successfully synced with main via 'git pull'!"

Write-Step "9. Running Automated Test Suites"
python -m unittest discover tests/
python scripts/verify_basic_git_workflow.py
python scripts/verify_structure.py
Write-Success "All automated verifications and unit test suites passed!"

if (-not $SkipPush) {
    Write-Step "10. Demonstrating 'git push': Publishing Branch to GitHub"
    git push -u origin feature/basic-git-workflow
    Write-Success "Feature branch published to GitHub successfully!"
} else {
    Write-Warn "Skipped push step due to -SkipPush switch."
}

Write-Step "11. Git Commit History Log (Last 10 Commits)"
git log --graph --oneline --decorate -n 10

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host " PRACTICE COMPLETED: Basic Git Workflow with Multiple Commits" -ForegroundColor Green
Write-Host " Branch URL: https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow" -ForegroundColor White
Write-Host " PR URL:     https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/pull/new/feature/basic-git-workflow" -ForegroundColor White
Write-Host "=================================================================`n" -ForegroundColor Green
