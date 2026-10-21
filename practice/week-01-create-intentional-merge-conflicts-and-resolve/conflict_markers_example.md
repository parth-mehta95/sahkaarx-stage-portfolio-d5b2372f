# Code Review Reference: Conflict Simulation & Resolution

This document serves as an explicit visual demonstration for code review of the intentional conflict and its resolution.

---

## 1. Conflicting Branches Overview

| Branch | Author Focus | Target File | Key Changes |
| :--- | :--- | :--- | :--- |
| `feature/jwt-auth` | Backend Auth Team | `auth_service.py` | Added secret key, HMAC-SHA256 JWT tokens, and token expiration. |
| `feature/oauth2-auth` | Integrations Team | `auth_service.py` | Added OAuth2 provider URL, bearer tokens, and OAuth scopes. |

---

## 2. Unresolved Conflict Markers (During Merge Attempt)

When `git merge feature/oauth2-auth` is executed on branch `feature/jwt-auth`:

```python
<<<<<<< HEAD
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
=======
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
>>>>>>> feature/oauth2-auth
```

---

## 3. Resolution Strategy (All Markers Removed)

In `auth_service.py`, both paradigms were integrated using a clean strategy pattern:

```python
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
            # JWT authentication logic
            ...
        elif strategy == "OAUTH2":
            # OAuth2 authentication logic
            ...
```

---

## 4. Git Graph Topology

```text
*   Merge branch 'feature/jwt-auth' into main (with resolved conflicts)
|\  
| *   fix(merge-conflict): resolve merge conflict between feature/jwt-auth and feature/oauth2-auth
| |\  
| | * feat(auth): implement OAuth2 and bearer token authentication with scopes (feature/oauth2-auth)
| * | feat(auth): implement JWT token authentication with expiration check (feature/jwt-auth)
| |/  
* | chore(init): add base AuthService and Week 01 practice documentation
|/  
* Initial commit
```
