import os
import sys
import urllib.request
import urllib.parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.vietlott_analytics_hub import VietlottAnalyzer
from models.xsm3mien_analyzer import LotteryRegionAnalyzer

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
            print("✅ Đã gửi báo cáo Telegram 3 Miền thành công!")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

def format_region_report(region_name, analyzer):
    prizes = analyzer.get_latest_prizes()
    heads, tails = analyzer.analyze_head_tail(prizes)
    lo_gan = analyzer.analyze_lo_gan()
    top_gan = list(lo_gan.items())[:3]
    
    report = f"📍 *{region_name}:*\n"
    report += f"  • Đầu câm: `{', '.join(heads) if heads else 'Không'}` | Đuôi câm: `{', '.join(tails) if tails else 'Không'}`\n"
    report += f"  • Top Lô Gan: " + ", ".join([f"`{k}` ({v}kỳ)" for k, v in top_gan]) + "\n"
    return report

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️ Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID.")
        return

    # 1. BÁO CÁO XỔ SỐ 3 MIỀN
    xsmb = LotteryRegionAnalyzer("Miền Bắc (XSMB)", "data/xsmb/xsmb.json")
    xsmt = LotteryRegionAnalyzer("Miền Trung (XSMT)", "data/xsmt/xsmt.json")
    xsmn = LotteryRegionAnalyzer("Miền Nam (XSMN)", "data/xsmn/xsmn.json")

    msg = "🇻🇳 *BÁO CÁO XỔ SỐ 3 MIỀN & VIETLOTT* 🇻🇳\n\n"
    msg += "🔥 *PHÂN TÍCH XỔ SỐ 3 MIỀN*\n"
    msg += format_region_report("XSMB", xsmb) + "\n"
    msg += format_region_report("XSMT", xsmt) + "\n"
    msg += format_region_report("XSMN", xsmn) + "\n"

    # 2. BÁO CÁO VIETLOTT
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

    msg += "🎰 *VÉ THÔNG MINH VIETLOTT*\n"
    msg += "🔴 *Mega 6/45:*\n"
    for idx, t in enumerate(get_tickets(analyzer_mega), 1):
        msg += f"`{idx}. {' - '.join(f'{x:02d}' for x in t)}` (Tổng: {sum(t)})\n"
        
    msg += "\n🔵 *Power 6/55:*\n"
    for idx, t in enumerate(get_tickets(analyzer_power), 1):
        msg += f"`{idx}. {' - '.join(f'{x:02d}' for x in t)}` (Tổng: {sum(t)})\n"

    send_telegram_message(bot_token, chat_id, msg)

if __name__ == "__main__":
    main()
