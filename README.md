# DiscoverU

An AI-powered profile analyzer built with FastAPI, Redis, and OAuth 2.0 (PKCE).

DiscoverU securely authenticates users via MAL using Oauth2, fetches profile data, and generates an AI-driven analysis using an LLM — all wrapped in a clean frontend interface.

---

##  Features

- **OAuth 2.0 with PKCE**
  - Secure authorization flow
  - CSRF protection using `state`
  - Code verifier & challenge implementation

- **Redis Session Management**
  - Server-side session storage
  - Access & refresh token handling
  - Automatic token refresh logic

- **LLM Integration**
  - Dynamic prompt generation
  - AI-generated profile analysis
  - Structured error handling for API failures

- **Rate Limiting**
  - Prevents abuse of analysis endpoint
  - Configured with `slowapi`
  - Graceful 429 error responses

- **Operational Logging**
  - Login attempts
  - Token exchange events
  - Analysis requests

## 🛠 Tech Stack

- **Backend:** FastAPI
- **Session Store:** Redis
- **Rate Limiting:** SlowAPI
- **Authentication:** OAuth 2.0 + PKCE
- **AI Integration:** LLM API
- **Frontend:** Vanilla HTML/CSS/JS
- **Environment Management:** python-dotenv

