# Thong Tin Deploy - Checkpoint 5

## Thong Tin Hoc Vien

| Muc | Noi dung |
|-----|----------|
| Ho va ten | Nguyen Thi Khanh Ly |
| mã học viên | 2A202601403 |
| Repo | https://github.com/ngnkhanhly7/K3-DAY12-2A202601403-NguyenThiKhanhLy |

## Service

| Muc | Noi dung |
|-----|----------|
| Public URL | https://k3-day12-2a202601403-nguyenthikhanhly-production.up.railway.app |
| Platform | Railway |
| Ngay deploy | 2026-08-10 |

## Bien Moi Truong Da Set Tren Cloud

Chi ghi ten bien, khong ghi gia tri secret.

| Bien | Da set | Ghi chu |
|------|--------|---------|
| `PORT` | yes | Railway tu gan |
| `AGENT_API_KEY` | yes | dat trong Railway Variables, khong ghi gia tri vao repo |
| `REDIS_URL` | yes | Redis add-on cua Railway |
| `RATE_LIMIT_PER_MINUTE` | yes | dat trong Railway Variables hoac dung default |
| `MONTHLY_BUDGET_USD` | yes | dat trong Railway Variables hoac dung default |
| `LOG_LEVEL` | yes | INFO |

## Lenh Kiem Tra

```powershell
$url = "https://k3-day12-2a202601403-nguyenthikhanhly-production.up.railway.app"

curl.exe -i "$url/health"
curl.exe -i "$url/ready"

curl.exe -i -X POST "$url/ask" `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"Hello\"}"

curl.exe -i -X POST "$url/ask" `
  -H "Content-Type: application/json" `
  -H "X-API-Key: $env:DEPLOY_API_KEY" `
  -H "X-User-Id: sv-test" `
  -d "{\"question\":\"Deploy la gi?\"}"
```

## Ket Qua Chay That

```text
GET /health -> 200 {"status":"ok","service":"day12-agent","version":"1.0.0"}
GET /ready -> 200 {"status":"ready","redis":true}
POST /ask without X-API-Key -> 401
POST /ask with X-API-Key -> 200
```

## Anh Chup Man Hinh

Dat anh minh chung trong thu muc `screenshots/`:

- `screenshots/dashboard.png`: dashboard Railway deploy thanh cong
- `screenshots/health.png`: ket qua goi `/health`, `/ready`, `/ask`
