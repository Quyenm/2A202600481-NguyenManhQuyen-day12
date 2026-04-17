# Lab 12 — Complete Production Agent

This project combines everything learned in Day 12 into one complete production-ready agent.

## Deliverable Checklist

- [x] Dockerfile (multi-stage, under 500 MB)
- [x] `docker-compose.yml` (agent + redis)
- [x] `.dockerignore`
- [x] Health check endpoint (`GET /health`)
- [x] Readiness endpoint (`GET /ready`)
- [x] API key authentication
- [x] Rate limiting
- [x] Cost guard
- [x] Configuration from environment variables
- [x] Structured logging
- [x] Graceful shutdown
- [x] Public deployment config ready (Railway / Render)

## Structure

```text
.
├── app/
│   ├── main.py         # Main entry point — combines all features
│   └── config.py       # 12-factor configuration
├── utils/
│   ├── __init__.py
│   └── agent.py        # OpenAI-backed EduGuide agent
├── Dockerfile          # Multi-stage, production-ready image
├── docker-compose.yml  # Full local stack
├── railway.toml        # Railway deployment
├── render.yaml         # Render deployment
├── .env.example        # Environment template
├── .dockerignore
├── check_production_ready.py
└── requirements.txt
```

## Run Locally

```bash
# 1. Setup
cp .env.example .env.local

# 2. Fill in real values
# OPENAI_API_KEY=...
# AGENT_API_KEY=...

# 3. Run with Docker Compose
docker compose up --build

# 4. Test
curl http://localhost:8000/health

# 5. Read the API key from .env.local and test the endpoint
API_KEY=$(grep AGENT_API_KEY .env.local | cut -d= -f2)
curl -H "X-API-Key: $API_KEY" \
     -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is deployment?"}'
```

## Deploy to Railway (< 5 minutes)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway variables set OPENAI_API_KEY=sk-...
railway variables set AGENT_API_KEY=your-secret-key
railway variables set JWT_SECRET=your-jwt-secret
railway up

# Get your public URL
railway domain
```

## Deploy to Render

1. Push the repository to GitHub
2. Open Render Dashboard → `New` → `Blueprint`
3. Connect the repository so Render reads `render.yaml`
4. Set secrets: `OPENAI_API_KEY`, `AGENT_API_KEY`, `JWT_SECRET`
5. Deploy and get your public URL

## Check Production Readiness

```bash
python check_production_ready.py
```

This script checks every item in the checklist and reports anything that is still missing.
