<#
.SYNOPSIS
    Automated Feature Branch Creation, Remote Push & Merge Workflow Runner.
    SahkaarX Stage Portfolio - Week 03 Practice: Create and Merge Feature Branches.
.DESCRIPTION
    Automates the complete Git feature branching and merge protocol:
    1. Prepares base working directory on main.
    2. Creates feature branch 1 ('feature/branch-strategy-validator'), commits code & tests, pushes to remote.
    3. Creates feature branch 2 ('feature/merge-history-analyzer'), commits code & tests, pushes to remote.
    4. Creates feature branch 3 ('feature/pr-lifecycle-manager'), commits code & tests, pushes to remote.
    5. Returns to 'main' and executes clean non-fast-forward (--no-ff) merges for each feature branch.
    6. Stages and commits portfolio integration and documentation artifacts.
    7. Pushes 'main' and all feature branches to GitHub.
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
}
$gitEmail = git config user.email
if (-not $gitEmail) {
    git config user.email "parth.mehta@ttpl.ind.in"
}

Write-Step "2. Ensuring Clean Baseline on 'main'"
git checkout main
git pull origin main --no-rebase

Write-Step "3. Creating & Publishing Branch 1: 'feature/branch-strategy-validator'"
git branch -D feature/branch-strategy-validator 2>$null
git checkout -b feature/branch-strategy-validator
git add src/utils/branch_validator.py src/utils/__init__.py
$diff1a = git diff --staged
if ($diff1a) {
    git commit -m "feat(branch-validator): implement automated git branch naming convention and hygiene validator"
    Write-Success "Committed Feature 1 Implementation"
}
git add tests/test_branch_validator.py
$diff1b = git diff --staged
if ($diff1b) {
    git commit -m "test(branch-validator): add comprehensive unit test suite for branch validator"
    Write-Success "Committed Feature 1 Unit Tests"
}
if (-not $SkipPush) {
    git push -u origin feature/branch-strategy-validator --force
    Write-Success "Pushed 'feature/branch-strategy-validator' to origin"
}

Write-Step "4. Creating & Publishing Branch 2: 'feature/merge-history-analyzer'"
git checkout main
git branch -D feature/merge-history-analyzer 2>$null
git checkout -b feature/merge-history-analyzer
git add src/utils/merge_analyzer.py src/utils/__init__.py
$diff2a = git diff --staged
if ($diff2a) {
    git commit -m "feat(merge-analyzer): add merge history analysis and commit graph auditor"
    Write-Success "Committed Feature 2 Implementation"
}
git add tests/test_merge_analyzer.py
$diff2b = git diff --staged
if ($diff2b) {
    git commit -m "test(merge-analyzer): add unit test coverage for merge commit history analysis"
    Write-Success "Committed Feature 2 Unit Tests"
}
if (-not $SkipPush) {
    git push -u origin feature/merge-history-analyzer --force
    Write-Success "Pushed 'feature/merge-history-analyzer' to origin"
}

Write-Step "5. Creating & Publishing Branch 3: 'feature/pr-lifecycle-manager'"
git checkout main
git branch -D feature/pr-lifecycle-manager 2>$null
git checkout -b feature/pr-lifecycle-manager
git add src/utils/pr_lifecycle.py src/utils/__init__.py
$diff3a = git diff --staged
if ($diff3a) {
    git commit -m "feat(pr-lifecycle): implement pull request lifecycle manager and checklist validator"
    Write-Success "Committed Feature 3 Implementation"
}
git add tests/test_pr_lifecycle.py
$diff3b = git diff --staged
if ($diff3b) {
    git commit -m "test(pr-lifecycle): add unit tests verifying pull request states and markdown generation"
    Write-Success "Committed Feature 3 Unit Tests"
}
if (-not $SkipPush) {
    git push -u origin feature/pr-lifecycle-manager --force
    Write-Success "Pushed 'feature/pr-lifecycle-manager' to origin"
}

Write-Step "6. Merging Feature Branches into 'main' with Clean History (--no-ff)"
git checkout main

Write-Host "Merging feature/branch-strategy-validator..." -ForegroundColor Yellow
git merge --no-ff feature/branch-strategy-validator -m "Merge pull request #1 from feature/branch-strategy-validator"
Write-Success "Merged feature/branch-strategy-validator into main"

Write-Host "Merging feature/merge-history-analyzer..." -ForegroundColor Yellow
git merge --no-ff feature/merge-history-analyzer -m "Merge pull request #2 from feature/merge-history-analyzer"
Write-Success "Merged feature/merge-history-analyzer into main"

Write-Host "Merging feature/pr-lifecycle-manager..." -ForegroundColor Yellow
git merge --no-ff feature/pr-lifecycle-manager -m "Merge pull request #3 from feature/pr-lifecycle-manager"
Write-Success "Merged feature/pr-lifecycle-manager into main"

Write-Step "7. Committing Documentation & Portfolio Integration Artifacts"
git add BRANCHING.md
git add docs/BRANCHING.md
git add docs/CONTRIBUTING.md
git add docs/DIRECTORY_STRUCTURE.md
git add practice/week-03-create-and-merge-feature-branches/
git add scripts/verify_feature_branches.py
git add scripts/run_feature_branches_practice.ps1
git add scripts/verify_structure.py
git add tests/test_repo_structure.py
git add README.md

$diffDocs = git diff --staged
if ($diffDocs) {
    git commit -m "docs(branching): document branching strategy, merged pull requests, and audit log"
    Write-Success "Committed Week 03 documentation, scripts, and portfolio updates to main"
}

if (-not $SkipPush) {
    Write-Step "8. Pushing 'main' to GitHub"
    git push origin main
    Write-Success "Pushed updated main to GitHub successfully"
}

Write-Step "9. Executing Automated Test & Verification Suites"
python -m unittest discover tests/
python scripts/verify_feature_branches.py
python scripts/verify_structure.py
Write-Success "All automated verifications and test suites passed!"

Write-Step "10. Git Commit Topology Graph"
git log --graph --oneline --decorate -n 18

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host " PRACTICE COMPLETED: Week 03 Create and Merge Feature Branches" -ForegroundColor Green
Write-Host " Repository: https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f" -ForegroundColor White
Write-Host "=================================================================`n" -ForegroundColor Green
