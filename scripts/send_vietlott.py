import os
import sys
import random
import urllib.request
import urllib.parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.vietlott_analytics_hub import VietlottAnalyzer

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
            print("✅ Đã gửi báo cáo Vietlott thành công!")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

def get_tickets(analyzer):
    tickets = []
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

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️ Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID.")
        return

    analyzer_mega = VietlottAnalyzer("Mega 6/45", 45, "data/vietlott/mega645_clean.txt")
    analyzer_power = VietlottAnalyzer("Power 6/55", 55, "data/vietlott/power655_clean.txt")

    msg = "🎰 *GỢI Ý VÉ THÔNG MINH VIETLOTT (20:00)* 🎰\n\n"
    msg += "🔴 *Mega 6/45:*\n"
    for idx, t in enumerate(get_tickets(analyzer_mega), 1):
        msg += f"`{idx}. {' - '.join(f'{x:02d}' for x in t)}` (Tổng: {sum(t)})\n"
        
    msg += "\n🔵 *Power 6/55:*\n"
    for idx, t in enumerate(get_tickets(analyzer_power), 1):
        msg += f"`{idx}. {' - '.join(f'{x:02d}' for x in t)}` (Tổng: {sum(t)})\n"

    send_telegram_message(bot_token, chat_id, msg)

if __name__ == "__main__":
    main()
