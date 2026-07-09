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

## Tech Stack

- **Backend:** FastAPI
- **Session Store:** Redis
- **Rate Limiting:** SlowAPI
- **Authentication:** OAuth 2.0 + PKCE
- **AI Integration:** LLM API
- **Frontend:** Vanilla HTML/CSS/JS
- **Environment Management:** python-dotenv


## Azure Practice Deployment details (Not online Due to credit limitations)

Deployment architecture on Azure:

* Azure App Service running the FastAPI backend
* Azure Cache for Redis for session storage
* Azure Key Vault for secrets management
* Private Endpoint + VNet integration for secure Redis access
* GitHub integration for Continuous deployment

<img width="1280" height="645" alt="image" src="https://github.com/user-attachments/assets/4e4f6013-56e3-40e0-b531-ca17ff4f7e82" />

<img width="1280" height="626" alt="image" src="https://github.com/user-attachments/assets/5a9a07f3-fd18-4c3f-ae1a-362b849ab4f3" />

<img width="1862" height="926" alt="image" src="https://github.com/user-attachments/assets/ab88c4e5-dc57-4420-8981-0b10b5d5df4f" />


