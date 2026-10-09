import os
import sys
import urllib.request
import urllib.parse

# Thêm thư mục gốc vào path để import các models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.vietlott_analytics_hub import VietlottAnalyzer
from models.xsmb_analyzer import XSMBAnalyzer

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
        print("⚠️ Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID.")
        return

    # 1. PHÂN TÍCH VIETLOTT
    analyzer_mega = VietlottAnalyzer("Mega 6/45", 45, "data/vietlott/mega645_clean.txt")
    analyzer_power = VietlottAnalyzer("Power 6/55", 55, "data/vietlott/power655_clean.txt")

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

    # 2. PHÂN TÍCH XSMB
    xsmb = XSMBAnalyzer("data/xsmb/xsmb.json")
    latest_prizes = xsmb.get_latest_prizes()
    heads_cam, tails_cam = xsmb.analyze_head_tail(latest_prizes)
    lo_gan = xsmb.analyze_lo_gan()
    top_gan = list(lo_gan.items())[:5]

    # 3. SOẠN TIN NHẮN TỔNG HỢP
    msg = "🎰 *BÁO CÁO PHÂN TÍCH XỔ SỐ TỔNG HỢP* 🎰\n\n"
    
    # Block XSMB
    msg += "🔴 *XỔ SỐ MIỀN BẮC (XSMB):*\n"
    msg += f"• Đầu câm: `{', '.join(heads_cam) if heads_cam else 'Không có'}`\n"
    msg += f"• Đuôi câm: `{', '.join(tails_cam) if tails_cam else 'Không có'}`\n"
    msg += "• Top 5 Lô Gan:\n"
    for num, count in top_gan:
        msg += f"  - Số `{num}`: gan `{count}` kỳ\n"
    msg += "\n"

    # Block Vietlott
    msg += "🔵 *VIETLOTT MEGA 6/45 - Top 5 Vé Gợi Ý:*\n"
    for idx, t in enumerate(mega_tickets, 1):
        t_str = " - ".join(f"{x:02d}" for x in t)
        msg += f"`{idx}. {t_str}` (Tổng: {sum(t)})\n"
        
    msg += "\n🟣 *VIETLOTT POWER 6/55 - Top 5 Vé Gợi Ý:*\n"
    for idx, t in enumerate(power_tickets, 1):
        t_str = " - ".join(f"{x:02d}" for x in t)
        msg += f"`{idx}. {t_str}` (Tổng: {sum(t)})\n"

    send_telegram_message(bot_token, chat_id, msg)

if __name__ == "__main__":
    main()
