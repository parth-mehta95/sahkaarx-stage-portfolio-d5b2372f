# Week 01: Merge Conflict Creation & Resolution

## Scenario Overview
This practice demonstrates professional Git conflict resolution skills for code review in a collaborative team environment.

## Repository Information
- **Portfolio Repository URL**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Target File**: [`auth_service.py`](auth_service.py)
- **Target Feature Branches**:
  1. `feature/jwt-auth`
  2. `feature/oauth2-auth`

---

## Step-by-Step Conflict Simulation Workflow

### 1. Base Setup (`main` branch)
Created base [`auth_service.py`](auth_service.py) with core `AuthService` interface:
```python
class AuthService:
    def __init__(self, service_name="SahkaarX-Auth"):
        self.service_name = service_name
        self.active_sessions = {}

    def authenticate_user(self, username, credential):
        ...
```

### 2. Feature Branch 1 (`feature/jwt-auth`)
Created branch `feature/jwt-auth` and implemented JWT token authentication with expiration checks and HMAC-SHA256 signature generation:
```bash
git checkout -b feature/jwt-auth
# Implemented JWT authentication in auth_service.py
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "feat(auth): implement JWT token authentication with expiration check"
```

### 3. Feature Branch 2 (`feature/oauth2-auth`)
Created branch `feature/oauth2-auth` from `main` and implemented OAuth2 / Bearer token authentication with scopes on the exact same methods:
```bash
git checkout main
git checkout -b feature/oauth2-auth
# Implemented OAuth2 authentication in auth_service.py
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "feat(auth): implement OAuth2 and bearer token authentication with scopes"
```

### 4. Triggering the Real Merge Conflict
Switched to `feature/jwt-auth` and executed merge with `feature/oauth2-auth`:
```bash
git checkout feature/jwt-auth
git merge feature/oauth2-auth
```
**Git Output:**
```text
Auto-merging practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
CONFLICT (content): Merge conflict in practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
Automatic merge failed; fix conflicts and then commit the result.
```

See [`conflict_markers_example.md`](conflict_markers_example.md) for detailed marker visualization (`<<<<<<< HEAD`, `=======`, `>>>>>>> feature/oauth2-auth`).

### 5. Resolving the Conflict
The conflict was resolved by harmonizing both authentication systems into a extensible multi-provider pattern, removing all Git conflict markers completely:
```bash
# Update auth_service.py with unified implementation
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "fix(merge-conflict): resolve merge conflict between feature/jwt-auth and feature/oauth2-auth with unified multi-strategy authentication"
```

### 6. Integration and GitHub Publishing
```bash
git checkout main
git merge --no-ff feature/jwt-auth -m "Merge branch 'feature/jwt-auth' into main (with resolved conflicts)"
git push origin main
git push -u origin feature/jwt-auth --force
git push -u origin feature/oauth2-auth --force
```

---

## Automated Execution Script
An automated PowerShell execution script is available at [`run_conflict_resolution.ps1`](../../scripts/run_conflict_resolution.ps1). Run it via:
```powershell
.\scripts\run_conflict_resolution.ps1
```

## Verification & Testing
Run unit tests to verify the resolved multi-strategy implementation:
```bash
python practice/week-01-create-intentional-merge-conflicts-and-resolve/test_auth_service.py
```
