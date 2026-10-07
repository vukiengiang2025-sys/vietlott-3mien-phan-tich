import json
import urllib.request
from rich.console import Console
from rich.panel import Panel

console = Console()

URL_MEGA = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
URL_POWER = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"

# Sử dụng đường dẫn tương đối ngay tại thư mục gốc của dự án
PATH_MEGA_JSONL = "power645.jsonl"
PATH_POWER_JSONL = "power655.jsonl"

PATH_MEGA_CLEAN = "mega645_clean.txt"
PATH_POWER_CLEAN = "power655_clean.txt"

def download_file(url, local_path):
    console.print(f"⏳ Đang tải dữ liệu từ GitHub: [cyan]{url}[/cyan]...")
    try:
        urllib.request.urlretrieve(url, local_path)
        console.print(f"✅ Đã tải và lưu thành công vào: [green]{local_path}[/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi khi tải file từ {url}:[/bold red] {e}")

def convert_jsonl_to_clean_txt(input_jsonl, output_txt):
    count = 0
    try:
        with open(input_jsonl, 'r', encoding='utf-8') as infile, \
             open(output_txt, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                if 'result' in data and len(data['result']) >= 6:
                    numbers = sorted(data['result'][:6])
                    formatted_line = " ".join(f"{num:02d}" for num in numbers)
                    outfile.write(formatted_line + "\n")
                    count += 1
        console.print(f"✨ Đã làm sạch [bold green]{count:,}[/bold green] kỳ quay -> [yellow]{output_txt}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi làm sạch file {input_jsonl}:[/bold red] {e}")

if __name__ == "__main__":
    console.print(Panel.fit("[bold green]TỰ ĐỘNG CẬP NHẬT & LÀM SẠCH DỮ LIỆU VIETLOTT[/bold green]", border_style="green"))
    download_file(URL_MEGA, PATH_MEGA_JSONL)
    download_file(URL_POWER, PATH_POWER_JSONL)
    convert_jsonl_to_clean_txt(PATH_MEGA_JSONL, PATH_MEGA_CLEAN)
    convert_jsonl_to_clean_txt(PATH_POWER_JSONL, PATH_POWER_CLEAN)
