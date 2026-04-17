# Lab 12 — Complete Production Agent

Kết hợp TẤT CẢ những gì đã học trong 1 project hoàn chỉnh.

## Checklist Deliverable

- [x] Dockerfile (multi-stage, < 500 MB)
- [x] docker-compose.yml (agent + redis)
- [x] .dockerignore
- [x] Health check endpoint (`GET /health`)
- [x] Readiness endpoint (`GET /ready`)
- [x] API Key authentication
- [x] Rate limiting
- [x] Cost guard
- [x] Config từ environment variables
- [x] Structured logging
- [x] Graceful shutdown
- [x] Public URL ready (Railway / Render config)

## Cấu Trúc

```text
06-lab-complete/
├── app/
│   ├── main.py         # Entry point — kết hợp tất cả
│   └── config.py       # 12-factor config
├── utils/
│   ├── __init__.py
│   └── agent.py        # OpenAI-backed EduGuide agent
├── Dockerfile          # Multi-stage, production-ready
├── docker-compose.yml  # Full stack
├── railway.toml        # Deploy Railway
├── render.yaml         # Deploy Render
├── .env.example        # Template
├── .dockerignore
├── check_production_ready.py
└── requirements.txt
```

## Chạy Local

```bash
# 1. Setup
cp .env.example .env.local

# 2. Điền giá trị thật
# OPENAI_API_KEY=...
# AGENT_API_KEY=...

# 3. Chạy với Docker Compose
docker compose up --build

# 4. Test
curl http://localhost:8000/health

# 5. Lấy API key từ .env.local, test endpoint
API_KEY=$(grep AGENT_API_KEY .env.local | cut -d= -f2)
curl -H "X-API-Key: $API_KEY" \
     -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is deployment?"}'
```

## Deploy Railway (< 5 phút)

```bash
# Cài Railway CLI
npm i -g @railway/cli

# Login và deploy
railway login
railway init
railway variables set OPENAI_API_KEY=sk-...
railway variables set AGENT_API_KEY=your-secret-key
railway variables set JWT_SECRET=your-jwt-secret
railway up

# Nhận public URL!
railway domain
```

## Deploy Render

1. Push repo lên GitHub
2. Render Dashboard → New → Blueprint
3. Connect repo → Render đọc `render.yaml`
4. Set secrets: `OPENAI_API_KEY`, `AGENT_API_KEY`, `JWT_SECRET`
5. Deploy → Nhận URL!

## Kiểm Tra Production Readiness

```bash
python check_production_ready.py
```

Script này kiểm tra tất cả items trong checklist và báo cáo những gì còn thiếu.
