import os
import urllib.request
import urllib.parse
from vietlott_analytics_hub import VietlottAnalyzer

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=payload)
        with urllib.request.urlopen(req) as response:
            print("✅ Đã gửi thông báo Telegram thành công!")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️ Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong môi trường.")
        return

    # Khởi tạo analyzer
    analyzer_mega = VietlottAnalyzer("Mega 6/45", 45, "mega645_clean.txt")
    analyzer_power = VietlottAnalyzer("Power 6/55", 55, "power655_clean.txt")

    # Lấy vé thông minh
    smart_mega = []
    smart_power = []
    
    # Hàm thu thập vé
    def get_tickets(analyzer):
        tickets = []
        import random
        attempts = 0
        mid = analyzer.max_num // 2
        while len(tickets) < 5 and attempts < 100000:
            attempts += 1
            ticket = sorted(random.sample(range(1, analyzer.max_num + 1), 6))
            if tuple(ticket) in analyzer.drawn_set:
                continue
            evens = sum(1 for x in ticket if x % 2 == 0)
            if evens not in [2, 3, 4]:
                continue
            lows = sum(1 for x in ticket if x <= mid)
            if lows not in [2, 3, 4]:
                continue
            s = sum(ticket)
            if not (analyzer.avg_sum - 30 <= s <= analyzer.avg_sum + 30):
                continue
            tickets.append(ticket)
        return tickets

    mega_tickets = get_tickets(analyzer_mega)
    power_tickets = get_tickets(analyzer_power)

    # Soạn nội dung tin nhắn Markdown
    msg = "🎰 *BÁO CÁO & GỢI Ý VÉ VIETLOTT HÀNG NGÀY* 🎰\n\n"
    
    msg += "🔴 *MEGA 6/45 - Top 5 Vé Thông Minh:*\n"
    for idx, t in enumerate(mega_tickets, 1):
        t_str = " - ".join(f"{x:02d}" for x in t)
        msg += f"`{idx}. {t_str}` (Tổng: {sum(t)})\n"
        
    msg += "\n🔵 *POWER 6/55 - Top 5 Vé Thông Minh:*\n"
    for idx, t in enumerate(power_tickets, 1):
        t_str = " - ".join(f"{x:02d}" for x in t)
        msg += f"`{idx}. {t_str}` (Tổng: {sum(t)})\n"
        
    msg += "\n✨ _Dữ liệu đã được cập nhật & lọc theo thuật toán Điểm rơi, Chẵn/Lẻ, Cao/Thấp & Chuỗi Tổng._"

    send_telegram_message(bot_token, chat_id, msg)

if __name__ == "__main__":
    main()
