import os
import json
import urllib.request
from rich.console import Console

console = Console()

# Nguồn dữ liệu
URL_MEGA = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
URL_POWER = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
URL_XSMB = "https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/main/data/xsmb.json"

# Đường dẫn lưu file
PATH_MEGA_CLEAN = "data/vietlott/mega645_clean.txt"
PATH_POWER_CLEAN = "data/vietlott/power655_clean.txt"
PATH_XSMB_JSON = "data/xsmb/xsmb.json"

def ensure_dirs():
    os.makedirs("data/vietlott", exist_ok=True)
    os.makedirs("data/xsmb", exist_ok=True)

def download_file(url, local_path):
    try:
        urllib.request.urlretrieve(url, local_path)
        console.print(f"✅ Đã tải: [green]{local_path}[/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi khi tải {url}:[/bold red] {e}")

def convert_vietlott_jsonl(input_jsonl, output_txt):
    count = 0
    try:
        if not os.path.exists(input_jsonl):
            return
        with open(input_jsonl, 'r', encoding='utf-8') as infile, \
             open(output_txt, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                if 'result' in data and len(data['result']) >= 6:
                    numbers = sorted(data['result'][:6])
                    outfile.write(" ".join(f"{num:02d}" for num in numbers) + "\n")
                    count += 1
        console.print(f"✨ Đã chuyển đổi [bold green]{count:,}[/bold green] kỳ Vietlott -> [yellow]{output_txt}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi làm sạch {input_jsonl}:[/bold red] {e}")

def run_pipeline():
    ensure_dirs()
    # Fetch Vietlott
    download_file(URL_MEGA, "data/vietlott/power645.jsonl")
    download_file(URL_POWER, "data/vietlott/power655.jsonl")
    convert_vietlott_jsonl("data/vietlott/power645.jsonl", PATH_MEGA_CLEAN)
    convert_vietlott_jsonl("data/vietlott/power655.jsonl", PATH_POWER_CLEAN)
def run_pipeline():
    ensure_dirs()
    # Fetch & Clean Vietlott
    download_file(URL_MEGA, "data/vietlott/power645.jsonl")
    download_file(URL_POWER, "data/vietlott/power655.jsonl")
    convert_vietlott_jsonl("data/vietlott/power645.jsonl", PATH_MEGA_CLEAN)
    convert_vietlott_jsonl("data/vietlott/power655.jsonl", PATH_POWER_CLEAN)
    
    # Xóa file thô tạm thời
    for tmp_file in ["data/vietlott/power645.jsonl", "data/vietlott/power655.jsonl"]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

    # Fetch XSMB
    download_file(URL_XSMB, PATH_XSMB_JSON)    

if __name__ == "__main__":
    run_pipeline()
