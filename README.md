![CI](https://github.com/ngnkhanhly7/K3-DAY12-2A202601403-NguyenThiKhanhLy/actions/workflows/ci.yml/badge.svg)

# K3 - Ngày 12: Hạ Tầng Cloud & Deployment

Repository bài lab triển khai một AI agent từ local lên môi trường cloud, có bảo mật API key, rate limit, cost guard, Redis state, Docker, health/readiness probe và CI/CD.

## Thông Tin

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Nguyễn Thị Khánh Ly |
| Mã học viên | 2A202601403 |
| Public URL | https://k3-day12-2a202601403-nguyenthikhanhly-production.up.railway.app |
| Platform | Railway |

## Chạy Local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Kiểm tra:

```powershell
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/ready
```

## Chạy Bằng Docker Compose

```powershell
docker compose up -d --scale agent=3
```

Nginx expose service tại:

```text
http://localhost:8000
```

## Live Endpoints

```powershell
$url = "https://k3-day12-2a202601403-nguyenthikhanhly-production.up.railway.app"

Invoke-WebRequest "$url/health"
Invoke-WebRequest "$url/ready"
```

Gọi `/ask` cần header `X-API-Key` khớp với `AGENT_API_KEY` trên Railway.

## Test

```powershell
$env:PYTHONIOENCODING='utf-8'
pytest tests/ -v
python grade.py
```

## Ghi Chú Bảo Mật

- Không commit `.env`.
- Chỉ commit `.env.example`.
- Secret deploy được đặt trong Railway Variables hoặc GitHub Actions Secrets.
- `AGENT_API_KEY` và `REDIS_URL` không được ghi giá trị thật vào repo.
