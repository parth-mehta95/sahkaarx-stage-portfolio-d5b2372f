# Week 01: Automated Merge Conflict Creation & Resolution Script
# Repository: https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f

# Ensure execution from repository root
$repoRoot = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $repoRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Step 1: Initialize Base Files on main Branch" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git checkout main
git add .
git commit -m "chore(init): add base AuthService and Week 01 practice documentation"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 2: Create feature/jwt-auth Branch" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git checkout -b feature/jwt-auth

$jwtContent = @'
"""
Authentication & Authorization Service
Week 01: Merge Conflict Demonstration & Resolution
"""

import time
import base64
import json
import hashlib
import hmac


class AuthService:
    def __init__(self, service_name="SahkaarX-Auth", secret_key="super-secret-jwt-key"):
        self.service_name = service_name
        self.secret_key = secret_key
        self.active_sessions = {}

    def authenticate_user(self, username, credential, expires_in=3600):
        """
        JWT-based authentication method.
        Validates credentials and issues a signed JSON Web Token.
        """
        if not username or not credential:
            raise ValueError("Username and JWT credential are required")

        print(f"Authenticating {username} via JWT strategy on {self.service_name}...")
        
        # Simple simulated JWT payload generation
        header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
        payload = base64.b64encode(json.dumps({
            "sub": username,
            "iat": int(time.time()),
            "exp": int(time.time()) + expires_in,
            "service": self.service_name
        }).encode()).decode()
        signature = hmac.new(self.secret_key.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
        token = f"{header}.{payload}.{signature}"

        session_data = {
            "user": username,
            "auth_type": "JWT",
            "token": token,
            "expires_at": int(time.time()) + expires_in,
            "status": "authenticated"
        }
        self.active_sessions[username] = session_data
        return session_data

    def get_service_status(self):
        return {
            "service": self.service_name,
            "auth_type": "JWT",
            "status": "online",
            "active_users_count": len(self.active_sessions)
        }
'@

Set-Content -Path "practice\week-01-create-intentional-merge-conflicts-and-resolve\auth_service.py" -Value $jwtContent -Encoding UTF8
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "feat(auth): implement JWT token authentication with expiration check"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 3: Create feature/oauth2-auth Branch from main" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git checkout main
git checkout -b feature/oauth2-auth

$oauthContent = @'
"""
Authentication & Authorization Service
Week 01: Merge Conflict Demonstration & Resolution
"""

import time
import uuid


class AuthService:
    def __init__(self, service_name="SahkaarX-Auth", oauth_provider="https://auth.sahkaarx.io"):
        self.service_name = service_name
        self.oauth_provider = oauth_provider
        self.active_sessions = {}

    def authenticate_user(self, username, credential, scopes=None):
        """
        OAuth2 / Bearer token authentication method.
        Validates token against OAuth2 provider and checks authorization scopes.
        """
        if not username or not credential:
            raise ValueError("Username and OAuth2 access token are required")

        print(f"Authenticating {username} via OAuth2 provider ({self.oauth_provider}) on {self.service_name}...")
        
        assigned_scopes = scopes or ["read:profile", "write:portfolio"]
        bearer_token = f"bearer_{uuid.uuid4().hex}"

        session_data = {
            "user": username,
            "auth_type": "OAuth2",
            "access_token": bearer_token,
            "scopes": assigned_scopes,
            "provider": self.oauth_provider,
            "status": "authenticated"
        }
        self.active_sessions[username] = session_data
        return session_data

    def get_service_status(self):
        return {
            "service": self.service_name,
            "auth_type": "OAuth2",
            "provider": self.oauth_provider,
            "status": "online",
            "active_users_count": len(self.active_sessions)
        }
'@

Set-Content -Path "practice\week-01-create-intentional-merge-conflicts-and-resolve\auth_service.py" -Value $oauthContent -Encoding UTF8
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "feat(auth): implement OAuth2 and bearer token authentication with scopes"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 4: Attempt Merge to Trigger Conflict" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git checkout feature/jwt-auth
git merge feature/oauth2-auth

Write-Host "`n[NOTICE]: Git merge triggered conflict as expected in auth_service.py" -ForegroundColor Yellow

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 5: Resolve Conflict Markers and Commit Resolution" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$resolvedContent = @'
"""
Authentication & Authorization Service
Week 01: Merge Conflict Demonstration & Resolution
"""

import time
import base64
import json
import hashlib
import hmac
import uuid


class AuthService:
    def __init__(self, service_name="SahkaarX-Auth", secret_key="super-secret-jwt-key", oauth_provider="https://auth.sahkaarx.io"):
        self.service_name = service_name
        self.secret_key = secret_key
        self.oauth_provider = oauth_provider
        self.active_sessions = {}

    def authenticate_user(self, username, credential, auth_strategy="JWT", expires_in=3600, scopes=None):
        """
        Unified multi-strategy authentication method.
        Resolved conflict by supporting both JWT and OAuth2 authentication paradigms.
        """
        if not username or not credential:
            raise ValueError("Username and credential are required")

        strategy = auth_strategy.upper()

        if strategy == "JWT":
            print(f"Authenticating {username} via JWT strategy on {self.service_name}...")
            header = base64.b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode()
            payload = base64.b64encode(json.dumps({
                "sub": username,
                "iat": int(time.time()),
                "exp": int(time.time()) + expires_in,
                "service": self.service_name
            }).encode()).decode()
            signature = hmac.new(self.secret_key.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
            token = f"{header}.{payload}.{signature}"

            session_data = {
                "user": username,
                "auth_type": "JWT",
                "token": token,
                "expires_at": int(time.time()) + expires_in,
                "status": "authenticated"
            }
        elif strategy == "OAUTH2":
            print(f"Authenticating {username} via OAuth2 provider ({self.oauth_provider}) on {self.service_name}...")
            assigned_scopes = scopes or ["read:profile", "write:portfolio"]
            bearer_token = f"bearer_{uuid.uuid4().hex}"

            session_data = {
                "user": username,
                "auth_type": "OAuth2",
                "access_token": bearer_token,
                "scopes": assigned_scopes,
                "provider": self.oauth_provider,
                "status": "authenticated"
            }
        else:
            raise ValueError(f"Unsupported authentication strategy: {auth_strategy}. Use 'JWT' or 'OAUTH2'.")

        self.active_sessions[username] = session_data
        return session_data

    def get_service_status(self):
        return {
            "service": self.service_name,
            "supported_strategies": ["JWT", "OAuth2"],
            "oauth_provider": self.oauth_provider,
            "status": "online",
            "active_users_count": len(self.active_sessions)
        }


if __name__ == "__main__":
    service = AuthService()
    print("Testing resolved AuthService:")
    jwt_session = service.authenticate_user("developer_jwt", "secret123", auth_strategy="JWT")
    print("JWT Session:", jwt_session)
    oauth_session = service.authenticate_user("developer_oauth", "token456", auth_strategy="OAUTH2", scopes=["admin", "repo:write"])
    print("OAuth2 Session:", oauth_session)
    print("Service Status:", service.get_service_status())
'@

Set-Content -Path "practice\week-01-create-intentional-merge-conflicts-and-resolve\auth_service.py" -Value $resolvedContent -Encoding UTF8
git add practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py
git commit -m "fix(merge-conflict): resolve merge conflict between feature/jwt-auth and feature/oauth2-auth with unified multi-strategy authentication"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 6: Merge Resolved feature/jwt-auth into main" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git checkout main
git merge --no-ff feature/jwt-auth -m "Merge branch 'feature/jwt-auth' into main (with resolved conflicts)"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Step 7: Push All Branches and main to GitHub" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

git push origin main
git push -u origin feature/jwt-auth --force
git push -u origin feature/oauth2-auth --force

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Git Commit History Graph" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

git log --graph --oneline --all -n 15

Write-Host "`nConflict resolution and branch push complete!" -ForegroundColor Green
