# Phiếu Phản Ánh - K3 Ngày 12

Họ và tên: Nguyễn Thị Khánh Ly  
Mã học viên: 2A202601403

---

### Câu 1 - Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi deploy lên Railway, nếu tôi quên set `AGENT_API_KEY`, app sẽ lỗi ngay lúc start thay vì chạy âm thầm với key mặc định. Nếu để `"changeme"`, service public vẫn online và người khác có thể đoán key để gọi `/ask`. Fail fast giúp tôi phát hiện thiếu secret ở bước deploy, trước khi API bị dùng sai.

---

### Câu 2 - Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi nêu hai việc bạn làm được với dòng log đó mà `print("đã trả lời xong")` không làm được.

> Log tôi thấy khi gọi `/ask` có dạng:
>
> `{"event":"ask_completed","level":"info","timestamp":"2026-08-10T...","user_id":"student","tokens_in":1,"tokens_out":35,"cost_usd":0.00002115}`
>
> Với log JSON, tôi có thể lọc theo `user_id` để xem riêng request của một người dùng, và có thể thống kê/tạo cảnh báo theo `cost_usd` hoặc token. Nếu chỉ `print("đã trả lời xong")` thì không biết request của ai, tốn bao nhiêu token, hay sự kiện xảy ra lúc nào.

---

### Câu 3 - Kích thước image (CP2)

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | khoảng 800MB-1GB |
| Multi-stage | 270MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Image multi-stage của tôi build ra khoảng 270MB (`day12-agent:cp2-test`). Bản 1-stage dùng `python:3.11` đầy đủ thường rất lớn vì mang theo nhiều thứ không cần cho runtime như tool build, cache cài đặt, metadata và toàn bộ context source. Multi-stage chỉ copy phần package đã install từ builder và source cần chạy (`app`, `utils`) sang image `python:3.11-slim`, nên image nhỏ hơn và ít bề mặt tấn công hơn.

---

### Câu 4 - Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt `COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Với Dockerfile hiện tại, các layer `COPY requirements.txt` và `RUN pip install --prefix=/install -r requirements.txt` được dùng lại từ cache nếu tôi chỉ sửa code trong `app/main.py`. Docker chỉ phải chạy lại từ layer `COPY app/ app/` trở đi và export image. Nếu đặt `COPY . .` trước `RUN pip install`, mỗi lần sửa một dòng code Docker sẽ coi context đã đổi và phải chạy lại `pip install`, làm build chậm hơn nhiều.

---

### Câu 5 - Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Nếu app Python có lỗi cho phép chạy lệnh hệ thống, kẻ tấn công có thể thực thi lệnh bên trong container. Nếu process chạy bằng root, các lệnh đó cũng chạy với quyền root trong container, nguy hiểm hơn nếu có mount volume hoặc lỗi escape container. Lệnh `USER appuser` làm uvicorn chạy bằng user thường, nên dù app bị khai thác thì quyền bị giới hạn, không phải root.

---

### Câu 6 - Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo phút đồng hồ reset lúc giây 00, một người dùng có thể gửi tối đa bao nhiêu request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được con số đó.

> Với fixed window theo phút đồng hồ, user có thể gửi 10 request ở giây 59 của phút trước, rồi ngay khi sang giây 00 gửi thêm 10 request nữa. Như vậy trong khoảng khoảng 2 giây họ gửi được 20 request mà vẫn không vi phạm từng "phút" riêng lẻ. Sliding window 60 giây chặn kiểu lách này vì nó luôn nhìn lại 60 giây gần nhất.

---

### Câu 7 - Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit bảo vệ tốc độ gọi API, còn cost guard bảo vệ ngân sách tiền/token. Rate limit có thể cho qua nếu user chỉ gọi 1 request/phút, nhưng cost guard vẫn phải chặn nếu các request trước đó đã tiêu quá `MONTHLY_BUDGET_USD`. Ngược lại, cost guard có thể còn dư ngân sách nhưng rate limit chặn nếu user bắn quá nhiều request liên tiếp trong 60 giây.

---

### Câu 8 - /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm 3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu endpoint duy nhất vừa là health vừa kiểm tra Redis, khi Redis mất kết nối 30 giây thì cả 3 container đều trả lỗi health. Orchestrator/load balancer sẽ nghĩ các container chết, rồi restart chúng liên tục. Trong lúc restart, các request đang xử lý bị gián đoạn và service chập chờn dù process Python vẫn còn sống. Tách `/health` và `/ready` giúp `/ready` ngắt traffic khi Redis lỗi, còn `/health` không phụ thuộc Redis nên tránh restart oan.

---

### Câu 9 - Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một `X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Khi state nằm trong Redis, các replica đều nhìn thấy cùng lịch sử nên `history_length` tăng theo các lượt trước đó, ví dụ lượt sau thấy các message user/assistant đã lưu. Nếu dùng dict Python trong RAM, request rơi vào container nào thì chỉ container đó nhớ lịch sử của nó. Khi Nginx round-robin sang container khác, `history_length` có thể quay lại 0 hoặc nhảy không đều, vì mỗi replica có bộ nhớ riêng.

---

### Câu 10 - Deploy thật (CP5)

Ghi lại một lỗi bạn gặp khi deploy lên cloud: thông báo lỗi là gì, bạn tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Khi deploy Railway tôi gặp lỗi `Healthcheck failed` ở bước `Network > Healthcheck`, dù build và deploy image đã xong. Tôi xem log Railway thấy healthcheck gọi `/health` nhưng retry window hết trước khi service healthy, và trước đó command start chưa chắc expand đúng `$PORT`. Tôi sửa `railway.toml` để start bằng `sh -c 'exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}'` và tăng `healthcheckTimeout` lên 60. Sau khi commit/push và redeploy, URL Railway trả `/health` 200, `/ready` 200, `/ask` thiếu key 401 và `/ask` có key 200.
