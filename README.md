# 🎰 Vietnam Lottery Analytics Hub (Vietlott & XS 3 Miền)

Hệ thống tự động thu thập, phân tích thống kê và gợi ý số thông minh cho **Vietlott (Mega 6/45, Power 6/55)** và **Xổ số Kiến thiết 3 Miền (XSMB, XSMT, XSMN)**. Hệ thống được tự động hóa hoàn toàn qua GitHub Actions và gửi báo cáo trực tiếp về Telegram.

---

## 🚀 Tính Năng Chính

### 1. Xổ Số 3 Miền (XSMB - XSMT - XSMN)
* **Thống kê Lô Gan:** Tìm danh sách các cặp số (00-99) chưa về lâu nhất.
* **Đầu / Đuôi Câm:** Nhận diện các chữ số hàng chục và hàng đơn vị không xuất hiện trong kỳ quay gần nhất.
* **Tần suất Lô Xiên 2:** Phân tích thuật toán tổ hợp các cặp lô hay nổ cùng nhau trong 30 kỳ gần nhất.

### 2. Vietlott Smart Tickets (Mega 6/45 & Power 6/55)
* **Thuật toán lọc vé thông minh:**
  * Bỏ các bộ số đã từng trúng giải Jackpot trong lịch sử.
  * Cân bằng tỷ lệ Chẵn/Lẻ ($2:4$, $3:3$, $4:2$).
  * Cân bằng khoảng Lớn/Nhỏ ($2:4$, $3:3$, $4:2$).
  * Tối ưu hóa tổng định lượng nằm trong khoảng độ lệch chuẩn ($\mu \pm 30$).

### 3. Tự Động Hóa 100% (CI/CD)
* **18:30 (Giờ VN):** Báo cáo Phân tích Xổ số 3 Miền gửi về Telegram.
* **20:00 (Giờ VN):** Báo cáo Gợi ý Vé thông minh Vietlott gửi về Telegram.

---

## 📂 Cấu Trúc Dự Án

```text
vietnam-lottery-analytics-hub/
├── .github/
│   └── workflows/
│       ├── cron_3mien.yml        # Workflow chạy lúc 18h30
│       └── cron_vietlott.yml     # Workflow chạy lúc 20h00
├── data/                         # Dữ liệu tự động cập nhật (.json, .txt)
│   ├── vietlott/
│   ├── xsmb/
│   ├── xsmt/
│   └── xsmn/
├── models/                       # Thuật toán phân tích
│   ├── vietlott_analytics_hub.py
│   └── xsm3mien_analyzer.py
├── scripts/                      # Scraper & Telegram Bot
│   ├── fetch_data.py
│   ├── send_3mien.py
│   └── send_vietlott.py
├── requirements.txt
└── README.md
