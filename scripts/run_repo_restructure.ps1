# Week 02: Automated Repository Restructuring & Atomic Commit Workflow
# Repository: https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f

$ErrorActionPreference = "Continue"

# Ensure execution from repository root
$repoRoot = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $repoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Step 1: Initialize / Checkout feature/repo-restructure" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$existingBranch = git branch --list "feature/repo-restructure"
if ($existingBranch) {
    Write-Host "Switching to existing branch 'feature/repo-restructure'..." -ForegroundColor Yellow
    git checkout feature/repo-restructure
} else {
    Write-Host "Creating new branch 'feature/repo-restructure'..." -ForegroundColor Green
    git checkout -b feature/repo-restructure
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 2: Atomic Commit 1 - Comprehensive .gitignore" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git add .gitignore
git commit -m "chore(git): establish comprehensive production-grade .gitignore"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 3: Atomic Commit 2 - Reorganize Scripts & Tooling" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Remove root loose script if tracked in git
if (Test-Path "run_conflict_resolution.ps1") {
    git rm -f "run_conflict_resolution.ps1"
}
git add scripts/
git commit -m "refactor(structure): reorganize scripts and add repository utility tooling"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 4: Atomic Commit 3 - Modular Source Package & Tests" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git add src/
git add tests/
git commit -m "feat(core): initialize modular src package with logging utilities and tests"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 5: Atomic Commit 4 - Documentation & Governance" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git add docs/
git add .github/
git commit -m "docs(architecture): add enterprise architecture, directory layout, and governance docs"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 6: Atomic Commit 5 - Practice Deliverable & Root Readme" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git add practice/
git add README.md
git commit -m "docs(practice): document week 02 restructure deliverable with git history and rationale"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 7: Run Automated Verification & Test Suite" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

python scripts/verify_structure.py
python -m unittest discover tests/

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 8: Push Feature Branch to GitHub" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git push -u origin feature/repo-restructure --force

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Commit History Graph (Last 10 Commits)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

git log --graph --oneline --all -n 10

Write-Host "`nRepository restructure and atomic push completed successfully!" -ForegroundColor Green
