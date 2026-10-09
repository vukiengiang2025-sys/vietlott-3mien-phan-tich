import os
import sys
import urllib.request
import urllib.parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
            print("✅ Đã gửi báo cáo Xổ số 3 Miền thành công!")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

def format_region_report(region_name, analyzer):
    prizes = analyzer.get_latest_prizes()
    heads, tails = analyzer.analyze_head_tail(prizes)
    lo_gan = analyzer.analyze_lo_gan()
    top_gan = list(lo_gan.items())[:3]
    top_xien2 = analyzer.analyze_lo_xien_2(limit_draws=30, top_k=3)
    
    report = f"📍 *{region_name}:*\n"
    report += f"  • Đầu câm: `{', '.join(heads) if heads else 'Không'}` | Đuôi câm: `{', '.join(tails) if tails else 'Không'}`\n"
    report += f"  • Top Lô Gan: " + ", ".join([f"`{k}` ({v}kỳ)" for k, v in top_gan]) + "\n"
    
    # Định dạng chuỗi hiển thị Lô Xiên 2
    xien_str_list = [f"`{p[0]}-{p[1]}` ({cnt}lần)" for p, cnt in top_xien2]
    report += f"  • Top Xiên 2 (30 kỳ): " + ", ".join(xien_str_list) + "\n"
    return report

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️ Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID.")
        return

    xsmb = LotteryRegionAnalyzer("Miền Bắc (XSMB)", "data/xsmb/xsmb.json")
    xsmt = LotteryRegionAnalyzer("Miền Trung (XSMT)", "data/xsmt/xsmt.json")
    xsmn = LotteryRegionAnalyzer("Miền Nam (XSMN)", "data/xsmn/xsmn.json")

    msg = "🇻🇳 *BÁO CÁO XỔ SỐ 3 MIỀN (18:30)* 🇻🇳\n\n"
    msg += format_region_report("XSMB", xsmb) + "\n"
    msg += format_region_report("XSMT", xsmt) + "\n"
    msg += format_region_report("XSMN", xsmn)

    send_telegram_message(bot_token, chat_id, msg)

if __name__ == "__main__":
    main()
