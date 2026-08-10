# Thong Tin Deploy - Checkpoint 5

## Thong Tin Hoc Vien

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Nguyễn Thị Khánh Ly |
| Mã học viên | 2A202601403 |
| Repo | https://github.com/ngnkhanhly7/K3-DAY12-2A202601403-NguyenThiKhanhLy |

## Service

| Muc | Noi dung |
|-----|----------|
| Public URL | Local fallback: http://localhost:8000 |
| Platform | Docker Compose local fallback with Nginx load balancer |
| Ngay deploy | 2026-08-10 |

## Bien Moi Truong Da Set

Chi ghi ten bien, khong ghi gia tri secret.

| Bien | Da set | Ghi chu |
|------|--------|---------|
| `PORT` | yes | default 8000 trong container |
| `AGENT_API_KEY` | yes | dat trong `.env`, khong ghi gia tri vao repo |
| `REDIS_URL` | yes | `redis://redis:6379/0` trong Docker Compose |
| `RATE_LIMIT_PER_MINUTE` | yes | dat trong `.env` hoac dung default |
| `MONTHLY_BUDGET_USD` | yes | dat trong `.env` hoac dung default |
| `LOG_LEVEL` | yes | dat trong `.env` hoac dung default |
| `LOCAL_FALLBACK` | yes | `true` de cham CP5 bang stack local |

## Lenh Kiem Tra

```powershell
docker compose up -d --scale agent=3

curl.exe -i http://localhost:8000/health
curl.exe -i http://localhost:8000/ready

curl.exe -i -X POST http://localhost:8000/ask `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"Hello\"}"

curl.exe -i -X POST http://localhost:8000/ask `
  -H "Content-Type: application/json" `
  -H "X-API-Key: $env:AGENT_API_KEY" `
  -H "X-User-Id: sv-test" `
  -d "{\"question\":\"Deploy la gi?\"}"
```

## Ket Qua Chay That

Local fallback duoc dung vi chua co phien deploy Railway/Render trong moi truong nay.
Stack chay bang Docker Compose, public gateway local la Nginx tai `http://localhost:8000`.

Ket qua mong doi:

```text
GET /health -> 200
GET /ready -> 200
POST /ask without X-API-Key -> 401
POST /ask with X-API-Key -> 200
```

## Anh Chup Man Hinh

Dat anh minh chung trong thu muc `screenshots/`, vi du:

- `screenshots/dashboard.png`: Docker Desktop hoac terminal `docker compose ps`
- `screenshots/health.png`: ket qua goi `/health`, `/ready`, `/ask`

## Neu Dung Phuong An Du Phong

Da dung local fallback do khong co thong tin dang nhap cloud Railway/Render trong phien lam viec nay. Bien `LOCAL_FALLBACK=true` da duoc dat trong `.env`.
