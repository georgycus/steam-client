# Steam Client Product Info Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fork `steam-next` into `steam-client` and add a narrow, production-usable API for SteamClient-platform auth, PICS app access tokens, and PICS product info.

**Architecture:** Reuse `steam-next` CM/protobuf/PICS implementation. Add SteamClient-platform authentication through `IAuthenticationService` and wire the resulting refresh token into `CMsgClientLogon.access_token`. Add a small facade that `steam-monitor` can call without knowing about low-level SteamClient details.

**Tech Stack:** Python 3.10+, `steam-next` codebase, gevent/protobuf client extra, pytest.

---

### Task 1: SteamClient refresh-token CM login

**Files:**
- Modify: `steam/client/__init__.py`
- Test: `tests/test_client_auth_token_login.py`

- [ ] Write tests proving `SteamClient.login_with_refresh_token()` fills `CMsgClientLogon.access_token` and does not put the refresh token into `password`.
- [ ] Run the test and verify it fails because the method does not exist.
- [ ] Add minimal `login_with_refresh_token(account_name, refresh_token, login_id=None)` implementation.
- [ ] Run the test and verify it passes.

### Task 2: SteamClient-platform web auth helper

**Files:**
- Modify: `steam/webauth.py`
- Test: `tests/test_webauth_steam_client_platform.py`

- [ ] Write tests proving credentials auth can be configured with `platform_type=1` and `website_id='Client'`.
- [ ] Run the test and verify it fails on current hard-coded web platform values.
- [ ] Add constructor options for platform type, website id, and friendly device name with current defaults preserved.
- [ ] Run the test and verify it passes.

### Task 3: Product info facade

**Files:**
- Create: `steam/product_info.py`
- Test: `tests/test_product_info.py`

- [ ] Write tests for `SteamProductInfoClient.get_product_info(app_ids)` using an injected Steam client factory.
- [ ] Run the test and verify it fails because the facade does not exist.
- [ ] Implement minimal facade: login with provided refresh token or username/password, request access tokens, request product info.
- [ ] Run the test and verify it passes.

### Task 4: Package metadata and docs

**Files:**
- Modify: `pyproject.toml`
- Modify: `README.md`

- [ ] Rename distribution metadata to `steam-client` while keeping the import package `steam`.
- [ ] Document install from git and minimal `SteamProductInfoClient` usage.
- [ ] Run package checks and tests.
