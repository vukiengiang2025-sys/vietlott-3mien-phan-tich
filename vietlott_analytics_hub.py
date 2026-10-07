import os
import math
import random
import itertools
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def nCr(n, r):
    return math.comb(n, r) if 0 <= r <= n else 0

def load_clean_data(filepath):
    tickets = []
    if not os.path.exists(filepath):
        return tickets
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 6:
                    tickets.append([int(p) for p in parts])
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi đọc file {filepath}:[/bold red] {e}")
    return tickets

class VietlottAnalyzer:
    def __init__(self, game_name, max_num, clean_filepath):
        self.game_name = game_name
        self.max_num = max_num
        self.clean_filepath = clean_filepath
        self.reload_data()

    def reload_data(self):
        """Tải lại dữ liệu mới nhất từ file text"""
        self.tickets = load_clean_data(self.clean_filepath)
        self.total_draws = len(self.tickets)
        self.total_possible = nCr(self.max_num, 6)
        self.drawn_set = set(tuple(t) for t in self.tickets)
        
        # Khung điểm rơi Top 3 lý thuyết
        self.peak_ranges = {}
        for i in range(1, 7):
            probs = {k: (nCr(k-1, i-1) * nCr(self.max_num-k, 6-i) / self.total_possible) * 100 for k in range(1, self.max_num + 1)}
            self.peak_ranges[i] = sorted(probs, key=probs.get, reverse=True)[:3]

        self.avg_sum = (1 + self.max_num) * 6 / 2

    # Ý TƯỞNG 1: Sinh vé theo Khung điểm rơi
    def generate_peak_tickets(self, count=5):
        console.rule(f"[bold cyan]1. VÉ THOẢ MÃN KHUNG ĐIỂM RƠI ({self.game_name})[/bold cyan]")
        valid_tickets = []
        for combo in itertools.product(*(self.peak_ranges[i] for i in range(1, 7))):
            if len(set(combo)) == 6 and list(combo) == sorted(combo):
                valid_tickets.append(combo)
                if len(valid_tickets) >= count:
                    break
        
        table = Table(title="🎲 Mẫu vé nằm trong Khung Điểm Rơi Tối Ưu")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("Bộ số", justify="center", style="bold green")
        for idx, t in enumerate(valid_tickets, 1):
            table.add_row(str(idx), " - ".join(f"{x:02d}" for x in t))
        console.print(table)

    # Ý TƯỞNG 2: Khoảng chênh lệch (Gap Analysis)
    def analyze_gaps(self):
        console.rule(f"[bold cyan]2. PHÂN TÍCH KHOẢNG CHÊNH LỆCH KỀ BÊN ({self.game_name})[/bold cyan]")
        if not self.tickets:
            console.print("[yellow]⚠️ Chưa có dữ liệu kỳ quay.[/yellow]")
            return

        gaps = []
        for t in self.tickets:
            for i in range(5):
                gaps.append(t[i+1] - t[i])
        gap_counts = Counter(gaps).most_common(5)
        
        table = Table(title="📊 Top 5 Khoảng cách (Δ) phổ biến giữa 2 số kế nhau")
        table.add_column("Khoảng cách", justify="center", style="yellow")
        table.add_column("Số lần xuất hiện", justify="right")
        table.add_column("Tỷ lệ (%)", justify="right", style="green")
        for gap, cnt in gap_counts:
            table.add_row(f"Cách nhau {gap} đơn vị", f"{cnt:,}", f"{(cnt/len(gaps))*100:.2f}%")
        console.print(table)

    # Ý TƯỞNG 3: Chẵn/Lẻ & Cao/Thấp
    def analyze_even_odd_high_low(self):
        console.rule(f"[bold cyan]3. TỶ LỆ CHẴN/LẺ VÀ CAO/THẤP ({self.game_name})[/bold cyan]")
        if not self.tickets:
            console.print("[yellow]⚠️ Chưa có dữ liệu kỳ quay.[/yellow]")
            return

        even_odd_patterns = Counter()
        mid = self.max_num // 2
        
        for t in self.tickets:
            evens = sum(1 for x in t if x % 2 == 0)
            even_odd_patterns[f"{evens} Chẵn - {6-evens} Lẻ"] += 1
            
        table = Table(title="☯️ Cấu trúc Chẵn/Lẻ phổ biến nhất")
        table.add_column("Dạng Cấu Trúc", justify="center", style="magenta")
        table.add_column("Số kỳ về", justify="right")
        table.add_column("Tỷ lệ (%)", justify="right", style="bold green")
        for pattern, cnt in even_odd_patterns.most_common(3):
            table.add_row(pattern, f"{cnt:,}", f"{(cnt/self.total_draws)*100:.2f}%")
        console.print(table)

    # Ý TƯỞNG 4: Tạo vé Thông Minh
    def generate_smart_tickets(self, count=5):
        console.rule(f"[bold cyan]4. TẠO VÉ THÔNG MINH (SMART TICKET GENERATOR - {self.game_name})[/bold cyan]")
        smart_tickets = []
        attempts = 0
        mid = self.max_num // 2
        
        while len(smart_tickets) < count and attempts < 100000:
            attempts += 1
            ticket = sorted(random.sample(range(1, self.max_num + 1), 6))
            t_tuple = tuple(ticket)
            
            if t_tuple in self.drawn_set:
                continue
            evens = sum(1 for x in ticket if x % 2 == 0)
            if evens not in [2, 3, 4]:
                continue
            lows = sum(1 for x in ticket if x <= mid)
            if lows not in [2, 3, 4]:
                continue
            s = sum(ticket)
            if not (self.avg_sum - 30 <= s <= self.avg_sum + 30):
                continue
                
            smart_tickets.append(ticket)

        table = Table(title=f"🧠 Top {len(smart_tickets)} Vé Thông Minh Được Sinh Ra")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("Bộ 6 số gợi ý", justify="center", style="bold yellow")
        table.add_column("Tổng chuỗi", justify="center", style="green")
        for idx, t in enumerate(smart_tickets, 1):
            table.add_row(str(idx), " - ".join(f"{x:02d}" for x in t), str(sum(t)))
        console.print(table)

    # Ý TƯỞNG 5: Số Nóng & Số Gan
    def analyze_hot_cold(self):
        console.rule(f"[bold cyan]5. SỐ NÓNG (HOT) VÀ SỐ GAN (COLD) ({self.game_name})[/bold cyan]")
        if not self.tickets:
            console.print("[yellow]⚠️ Chưa có dữ liệu kỳ quay.[/yellow]")
            return

        last_seen = {}
        recent_30 = Counter()
        for t in self.tickets[-30:]:
            recent_30.update(t)
        for idx, t in enumerate(reversed(self.tickets)):
            for num in t:
                if num not in last_seen:
                    last_seen[num] = idx
        
        table = Table(title="🔥 Top 5 Số Nóng (30 kỳ qua) & ❄️ Top 5 Số Gan (Lâu chưa về)")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("Số Nóng", justify="center", style="bold red")
        table.add_column("Số Gan", justify="center", style="bold blue")
        hot_top = recent_30.most_common(5)
        cold_top = sorted(last_seen.items(), key=lambda x: x[1], reverse=True)[:5]
        for i in range(5):
            h_str = f"Số {hot_top[i][0]:02d} ({hot_top[i][1]} lần)" if i < len(hot_top) else "-"
            c_str = f"Số {cold_top[i][0]:02d} ({cold_top[i][1]} kỳ)" if i < len(cold_top) else "-"
            table.add_row(str(i+1), h_str, c_str)
        console.print(table)

    # Ý TƯỞNG 6: Tổng Chuỗi Số (Sum Range) - Đã sửa lỗi ZeroDivisionError
    def analyze_sum_range(self):
        console.rule(f"[bold cyan]6. TỔNG CHUỖI SỐ - SUM RANGE ({self.game_name})[/bold cyan]")
        if not self.tickets:
            console.print("[yellow]⚠️ Chưa có dữ liệu kỳ quay.[/yellow]")
            return

        sums = [sum(t) for t in self.tickets]
        avg_s = sum(sums) / len(sums)
        table = Table(title="🧮 Thống kê Tổng 6 số")
        table.add_column("Chỉ số", style="dim")
        table.add_column("Giá trị", justify="right", style="bold yellow")
        table.add_row("Tổng trung bình thực tế", f"{avg_s:.1f}")
        table.add_row("Tổng nhỏ nhất / lớn nhất", f"{min(sums)} / {max(sums)}")
        table.add_row("Vùng Tổng Chuẩn (68% phổ biến)", f"{int(avg_s-30)} đến {int(avg_s+30)}")
        console.print(table)

    # Ý TƯỞNG 9: Cặp số hay đi cùng nhau
    def analyze_pairs(self):
        console.rule(f"[bold cyan]9. CẶP SỐ SONG HÀNH (PAIRS) ({self.game_name})[/bold cyan]")
        if not self.tickets:
            console.print("[yellow]⚠️ Chưa có dữ liệu kỳ quay.[/yellow]")
            return

        pairs = Counter()
        for t in self.tickets:
            for p in itertools.combinations(t, 2):
                pairs[p] += 1
        table = Table(title="👩‍❤️‍👨 Top 5 Cặp số hay về cùng nhau nhất")
        table.add_column("Cặp số", justify="center", style="bold cyan")
        table.add_column("Số kỳ xuất hiện", justify="right", style="green")
        for pair, cnt in pairs.most_common(5):
            table.add_row(f"{pair[0]:02d} - {pair[1]:02d}", f"{cnt} kỳ")
        console.print(table)

    # Ý TƯỞNG 10: Đánh giá Điểm Vé Tự Chọn (Ticket Scorer)
    def score_ticket(self, user_ticket):
        console.rule(f"[bold cyan]10. ĐÁNH GIÁ ĐIỂM CHẤT LƯỢNG VÉ TỰ CHỌN ({self.game_name})[/bold cyan]")
        user_ticket = sorted(user_ticket)
        score = 100
        reasons = []
        
        if tuple(user_ticket) in self.drawn_set:
            score -= 50
            reasons.append("❌ Vé ĐÃ TỪNG XỔ trong lịch sử (-50d)")
        else:
            reasons.append("✅ Vé chưa từng xuất hiện (+0d)")
            
        out_peak = sum(1 for i in range(6) if user_ticket[i] not in self.peak_ranges[i+1])
        if out_peak > 0:
            score -= out_peak * 8
            reasons.append(f"⚠️ Có {out_peak} vị trí nằm ngoài Vùng Điểm Rơi (-{out_peak*8}d)")
        else:
            reasons.append("✅ Tất cả 6 vị trí chuẩn Vùng Điểm Rơi (+0d)")

        s = sum(user_ticket)
        if not (self.avg_sum - 35 <= s <= self.avg_sum + 35):
            score -= 15
            reasons.append(f"⚠️ Tổng chuỗi {s} lệch xa Vùng Chuẩn (-15d)")
            
        table = Table(title=f"🎯 Chấm điểm Vé: [{' - '.join(f'{x:02d}' for x in user_ticket)}]")
        table.add_column("Tiêu chí", style="dim")
        table.add_column("Đánh giá & Trừ điểm", style="bold yellow")
        for r in reasons:
            parts = r.split("(")
            table.add_row(parts[0], "(" + parts[1] if len(parts)>1 else "")
        console.print(table)
        
        color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        console.print(Panel(f"[bold {color}]TỔNG ĐIỂM CHẤT LƯỢNG: {score} / 100 ĐIỂM[/bold {color}]", border_style=color))

    def run_all(self):
        self.generate_peak_tickets(5)
        self.analyze_gaps()
        self.analyze_even_odd_high_low()
        self.generate_smart_tickets(5)
        self.analyze_hot_cold()
        self.analyze_sum_range()
        self.analyze_pairs()

def main_menu():
    mega_path = "mega645_clean.txt"
    power_path = "power655_clean.txt"
    
    analyzer_mega = VietlottAnalyzer("Mega 6/45", 45, mega_path)
    analyzer_power = VietlottAnalyzer("Power 6/55", 55, power_path)

    while True:
        console.clear()
        console.print(Panel.fit(
            "[bold green]🎛️ MENU TRUNG TÂM PHÂN TÍCH VIETLOTT (10 IN 1)[/bold green]\n"
            "[yellow]1.[/yellow] 🔄 Cập nhật dữ liệu từ GitHub & Làm sạch\n"
            "[yellow]2.[/yellow] 📊 Phân tích TOÀN BỘ Mega 6/45\n"
            "[yellow]3.[/yellow] ⚡ Phân tích TOÀN BỘ Power 6/55\n"
            "[yellow]4.[/yellow] 🧠 Tạo Vé Thông Minh (Smart Generator)\n"
            "[yellow]5.[/yellow] 🎯 Chấm điểm 1 vé tự chọn bất kỳ\n"
            "[yellow]0.[/yellow] 🚪 Thoát",
            border_style="green"
        ))
        
        choice = input("👉 Nhập lựa chọn của bạn (0-5): ").strip()
        
        if choice == '1':
            os.system("python3 ~/test/update_and_clean.py")
            # Tải lại dữ liệu sau khi cập nhật file
            analyzer_mega.reload_data()
            analyzer_power.reload_data()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '2':
            analyzer_mega.run_all()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '3':
            analyzer_power.run_all()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '4':
            analyzer_mega.generate_smart_tickets(5)
            analyzer_power.generate_smart_tickets(5)
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '5':
            raw = input("Nhập 6 số (ví dụ: 5 12 19 24 35 41): ").strip()
            try:
                nums = [int(x) for x in raw.replace(',', ' ').split()]
                if len(nums) == 6:
                    analyzer_mega.score_ticket(nums)
                else:
                    print("⚠️ Vui lòng nhập đúng 6 số!")
            except:
                print("⚠️ Định dạng không hợp lệ!")
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '0':
            console.print("[bold yellow]Cảm ơn bạn đã sử dụng chương trình![/bold yellow]")
            break

if __name__ == "__main__":
    main_menu()
