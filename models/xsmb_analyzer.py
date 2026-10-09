import json
import os

class XSMBAnalyzer:
    def __init__(self, json_path="data/xsmb/xsmb.json"):
        self.json_path = json_path
        self.draws = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.json_path):
            return
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.draws = data
                elif isinstance(data, dict):
                    self.draws = list(data.values())
        except Exception as e:
            print(f"Lỗi đọc dữ liệu XSMB: {e}")

    def _extract_2digit_numbers(self, draw_obj):
        """Hàm phụ trợ: Rút trích 2 số cuối từ tất cả các giải của 1 kỳ quay"""
        numbers = []
        if not isinstance(draw_obj, dict):
            return numbers

        # Duyệt qua tất cả các trường chứa giải thưởng
        for key, value in draw_obj.items():
            if key in ['date', 'day', 'id', '_id']:
                continue
            if isinstance(value, list):
                for item in value:
                    item_str = str(item).strip()
                    if len(item_str) >= 2 and item_str.isdigit():
                        numbers.append(f"{int(item_str[-2:]):02d}")
            elif isinstance(value, (str, int)):
                val_str = str(value).strip()
                if len(val_str) >= 2 and val_str.isdigit():
                    numbers.append(f"{int(val_str[-2:]):02d}")
        return numbers

    def get_latest_prizes(self):
        """Lấy danh sách 2 số cuối của kỳ mới nhất"""
        if not self.draws:
            return []
        return self._extract_2digit_numbers(self.draws[0])

    def analyze_head_tail(self, latest_numbers):
        """Thống kê đầu / đuôi câm"""
        if not latest_numbers:
            return [], []
        heads = set(n[0] for n in latest_numbers)
        tails = set(n[1] for n in latest_numbers)
        
        missing_heads = sorted([str(i) for i in range(10) if str(i) not in heads])
        missing_tails = sorted([str(i) for i in range(10) if str(i) not in tails])
        return missing_heads, missing_tails

    def analyze_lo_gan(self, limit_draws=100):
        """Thống kê Lô Gan (00-99)"""
        if not self.draws:
            return {}
        
        last_seen = {}
        target_draws = self.draws[:limit_draws]
        
        for idx, draw in enumerate(target_draws):
            numbers_in_draw = set(self._extract_2digit_numbers(draw))
            for num_int in range(100):
                num_str = f"{num_int:02d}"
                if num_str not in last_seen and num_str in numbers_in_draw:
                    last_seen[num_str] = idx

        gan_dict = {}
        for num_int in range(100):
            num_str = f"{num_int:02d}"
            gan_dict[num_str] = last_seen.get(num_str, limit_draws)
            
        return dict(sorted(gan_dict.items(), key=lambda x: x[1], reverse=True))
