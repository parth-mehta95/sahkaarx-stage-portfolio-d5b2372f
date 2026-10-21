"""
Unit Test Suite for Resolved AuthService
Week 01: Merge Conflict Demonstration & Resolution
"""

from auth_service import AuthService


def test_auth_service():
    service = AuthService()

    # 1. Test JWT authentication strategy (from feature/jwt-auth)
    print("Testing JWT Authentication...")
    jwt_res = service.authenticate_user("developer_alice", "jwt-credential-123", auth_strategy="JWT", expires_in=1800)
    assert jwt_res["status"] == "authenticated", "JWT authentication failed"
    assert jwt_res["auth_type"] == "JWT"
    assert "token" in jwt_res
    assert len(jwt_res["token"].split(".")) == 3, "Invalid JWT token structure"
    print("✓ JWT Authentication passed successfully.")

    # 2. Test OAuth2 authentication strategy (from feature/oauth2-auth)
    print("\nTesting OAuth2 Authentication...")
    scopes = ["read:profile", "write:portfolio", "admin:access"]
    oauth_res = service.authenticate_user("developer_bob", "oauth-token-xyz", auth_strategy="OAUTH2", scopes=scopes)
    assert oauth_res["status"] == "authenticated", "OAuth2 authentication failed"
    assert oauth_res["auth_type"] == "OAuth2"
    assert "access_token" in oauth_res
    assert oauth_res["scopes"] == scopes
    print("✓ OAuth2 Authentication passed successfully.")

    # 3. Test Service Status
    print("\nTesting Service Status...")
    status = service.get_service_status()
    assert status["status"] == "online"
    assert status["active_users_count"] == 2
    assert "JWT" in status["supported_strategies"] and "OAuth2" in status["supported_strategies"]
    print("✓ Service status verification passed.")

    print("\nAll authentication strategy tests passed cleanly!")


if __name__ == "__main__":
    test_auth_service()
