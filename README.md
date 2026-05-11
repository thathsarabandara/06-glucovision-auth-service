<div align="center">

# 🔐 GlucoVision Auth Service

**The security perimeter and identity provider for the entire GlucoVision platform.**  
*JWT · OAuth2 · RBAC · MFA · Redis token blacklist*

[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)](#)
[![Redis](https://img.shields.io/badge/Redis-Token%20Store-DC382D?style=for-the-badge&logo=redis)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Credentials-4169E1?style=for-the-badge&logo=postgresql)](#)
[![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?style=for-the-badge&logo=docker)](#)
[![Status](https://img.shields.io/badge/Status-In%20Development-f59e0b?style=for-the-badge)](#)

</div>

---

## 📌 Purpose

GlucoVision Auth Service is the **security-critical authentication and authorization backbone** for the entire platform. Every other service delegates identity verification to this one. It exists as a separate repo because security vulnerabilities have their own lifecycle — a JWT library CVE must be patchable and deployable without touching patient data, food recognition models, or any other service.

> **Independent deployability is a patient safety requirement.** This service can be rolled back without affecting any other service.

---

## 📁 Project Structure

```
06-glucovision-auth-service/
└── (Git repository initialised — structure to be scaffolded)
```

> **Note:** This repository is in the initialisation phase. The service will be scaffolded using FastAPI when Phase 1 development begins.

---

## ✨ Planned Features (by phase)

### Phase 1 — Core Auth *(Foundation)*
- [ ] Email + password registration and login
- [ ] JWT issuance (RS256 asymmetric signing)
- [ ] Access token (15 min) + Refresh token (7 days)
- [ ] Token validation endpoint for gateway ForwardAuth
- [ ] RBAC: patient / clinician / admin / researcher roles

### Phase 2 — Social Login
- [ ] OAuth2 authorization code flow (Google)
- [ ] OAuth2 authorization code flow (Apple)
- [ ] Account linking (social → existing account)

### Phase 3 — MFA & Security
- [ ] TOTP multi-factor authentication (Google Authenticator)
- [ ] Biometric token support (mobile)
- [ ] Redis-backed token blacklist for instant logout
- [ ] Rate limiting: 5 login attempts / 15 min / IP

### Phase 4 — Session Management
- [ ] Web dashboard session management
- [ ] Token revocation broadcast via Redis pub/sub
- [ ] Password reset via email (SendGrid)

---

## 🚀 Getting Started

### Prerequisites

- Python ≥ 3.11
- PostgreSQL ≥ 15
- Redis ≥ 7
- Docker & Docker Compose

### Setup (once scaffolded)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8001

# Or via Docker Compose
docker compose up --build
```

---

## 🏗️ Planned Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python) |
| JWT | python-jose / PyJWT |
| Password Hashing | bcrypt (passlib) |
| OAuth2 | authlib |
| TOTP | pyotp |
| Token Store | Redis (redis-py) |
| Database | PostgreSQL (SQLAlchemy + Alembic) |
| Containerisation | Docker |

---

## 🔗 Service Dependencies

| Service | Interaction |
|---|---|
| `05` api-gateway | ForwardAuth calls this service to validate every request |
| `07` user-service | Fetches user profile on login (role assignment) |
| Google / Apple OAuth | External IdP for social login |
| SMTP / SendGrid | Email verification, password reset |
| Redis | Token blacklist, session state |
| PostgreSQL | User credential store |

---

## 🔐 Security Architecture

| Concern | Detail |
|---|---|
| JWT signing | RS256 (asymmetric) — private key signs, all services validate with public key |
| Token expiry | Access: 15 min · Refresh: 7 days |
| Token revocation | jti (JWT ID) stored in Redis blacklist on logout |
| RBAC | Role claim in JWT; gateway enforces route-level rules |
| Password policy | Minimum 12 chars, bcrypt cost factor 12 |
| MFA | TOTP required for clinician + admin roles |
| Secrets | Private key stored in HashiCorp Vault — never in env file |

---

## 🌐 API Endpoints (Planned)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | New user registration |
| `POST` | `/auth/login` | Email + password login → JWT |
| `POST` | `/auth/refresh` | Refresh access token |
| `POST` | `/auth/logout` | Revoke token (blacklist) |
| `POST` | `/auth/validate` | Token validation (ForwardAuth) |
| `GET` | `/auth/oauth2/google` | Google OAuth2 redirect |
| `POST` | `/auth/mfa/setup` | TOTP secret generation |
| `POST` | `/auth/mfa/verify` | TOTP code verification |

---

## 🧪 Testing (Planned)

```bash
# Unit tests
pytest tests/unit/

# Integration tests (full auth flow)
pytest tests/integration/

# Security tests
pytest tests/security/
```

| Test Type | Approach |
|---|---|
| Unit Tests | Token generation, RBAC logic, password hashing |
| Integration Tests | Login → token → refresh → logout → blacklist |
| Security Tests | Expired token rejection, tampered JWT, brute-force lockout |
| Penetration | OWASP API Security Top 10 checks |

---

<div align="center">

*Part of the [GlucoVision Platform](../01-glucovision-platform-architecture) — 21-Repo AI Diabetes Management System*

</div>
