import itertools
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track

console = Console()

def generate_all_combinations(max_number, pick=6):
    """Tạo tất cả các bộ 6 số từ 1 đến max_number"""
    return set(itertools.combinations(range(1, max_number + 1), pick))

def load_drawn_numbers_from_file(filepath):
    """
    Đọc file dữ liệu kết quả đã xổ.
    Giả định mỗi dòng trong file chứa 6 số phân cách bằng dấu phẩy, khoảng trắng hoặc tab.
    Ví dụ dòng trong file: 01 05 12 23 34 45
    """
    drawn = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Tách số theo dấu phẩy hoặc khoảng trắng
                parts = line.replace(',', ' ').split()
                if len(parts) >= 6:
                    try:
                        # Lấy 6 số đầu tiên, ép kiểu int và sắp xếp thành tuple
                        numbers = tuple(sorted([int(p) for p in parts[:6]]))
                        drawn.add(numbers)
                    except ValueError:
                        continue
    except FileNotFoundError:
        console.print(f"[bold red]Lỗi:[/bold red] Không tìm thấy file '{filepath}'.")
    return drawn

def format_ticket(numbers):
    """Định dạng bộ số ra chuỗi đẹp mắt: 01 - 05 - 12 - 23 - 34 - 45"""
    return " - ".join(f"{num:02d}" for num in numbers)

def analyze_lottery(game_name, max_num, filepath, sample_limit=10):
    console.rule(f"[bold cyan]Phân tích kết quả {game_name}[/bold cyan]")
    
    # 1. Tạo tất cả kết quả có thể
    console.print(f"⏳ Đang khởi tạo toàn bộ tập hợp 6/{max_num}...", end="\r")
    all_possible = generate_all_combinations(max_num, 6)
    total_possible = len(all_possible)
    
    # 2. Đọc dữ liệu đã xổ
    drawn = load_drawn_numbers_from_file(filepath)
    total_drawn = len(drawn)
    
    # 3. Lọc ra các bộ số chưa từng xuất hiện
    never_drawn = all_possible - drawn
    total_never = len(never_drawn)
    
    # 4. Hiển thị bảng thống kê
    stats_table = Table(title=f"📊 Bảng thống kê {game_name}", show_header=True, header_style="bold magenta")
    stats_table.add_column("Chỉ số", style="dim", width=25)
    stats_table.add_column("Giá trị", justify="right")
    stats_table.add_column("Tỷ lệ (%)", justify="right")

    stats_table.add_row("Tổng bộ số có thể có", f"{total_possible:,}", "100.00%")
    stats_table.add_row("Số kỳ đã xổ (Đã trúng)", f"{total_drawn:,}", f"{(total_drawn/total_possible)*100:.4f}%")
    stats_table.add_row("Số bộ CHƯA TỪNG xổ", f"{total_never:,}", f"{(total_never/total_possible)*100:.4f}%", style="bold green")

    console.print(stats_table)
    
    # 5. Mẫu một số bộ số chưa từng xổ
    if total_never > 0:
        sample_list = list(never_drawn)[:sample_limit]
        sample_table = Table(title=f"🎲 Mẫu {len(sample_list)} bộ số CHƯA TỪNG xuất hiện", header_style="bold yellow")
        sample_table.add_column("STT", justify="center", style="cyan")
        sample_table.add_column("Bộ 6 số", justify="center", style="bold white")
        
        for idx, ticket in enumerate(sample_list, 1):
            sample_table.add_row(str(idx), format_ticket(ticket))
            
        console.print(sample_table)
    console.print("\n")

if __name__ == "__main__":
    console.print(Panel.fit("[bold green]CHƯƠNG TRÌNH LỌC BỘ SỐ VIETLOTT CHƯA TỪNG XỔ[/bold green]", border_style="green"))
    
    # Đổi đường dẫn tới 2 file dữ liệu của bạn ở đây
    mega_file = "power645.jsonl"
    power_file = "power655.jsonl"
    
    # Chạy phân tích Mega 6/45
    analyze_lottery("Mega 6/45", 45, mega_file, sample_limit=5)
    
    # Chạy phân tích Power 6/55
    analyze_lottery("Power 6/55", 55, power_file, sample_limit=5)
