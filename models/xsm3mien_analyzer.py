import json
import os
from collections import Counter
from itertools import combinations

class LotteryRegionAnalyzer:
    def __init__(self, region_name, json_path):
        self.region_name = region_name
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
            print(f"Lỗi đọc dữ liệu {self.region_name}: {e}")

    def _extract_2digit_numbers(self, draw_obj):
        numbers = []
        if not isinstance(draw_obj, dict):
            return numbers

        def extract_recursive(val):
            if isinstance(val, list):
                for item in val:
                    extract_recursive(item)
            elif isinstance(val, dict):
                for v in val.values():
                    extract_recursive(v)
            elif isinstance(val, (str, int)):
                val_str = str(val).strip()
                if len(val_str) >= 2 and val_str.isdigit():
                    numbers.append(f"{int(val_str[-2:]):02d}")

        extract_recursive(draw_obj)
        return numbers

    def get_latest_prizes(self):
        if not self.draws:
            return []
        return self._extract_2digit_numbers(self.draws[0])

    def analyze_head_tail(self, latest_numbers):
        if not latest_numbers:
            return [], []
        heads = set(n[0] for n in latest_numbers)
        tails = set(n[1] for n in latest_numbers)
        
        missing_heads = sorted([str(i) for i in range(10) if str(i) not in heads])
        missing_tails = sorted([str(i) for i in range(10) if str(i) not in tails])
        return missing_heads, missing_tails

    def analyze_lo_gan(self, limit_draws=60):
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

    # ==================== TÍNH NĂNG MỚI BỔ SUNG ====================
    def analyze_lo_xien_2(self, limit_draws=30, top_k=5):
        """
        Thống kê Top K cặp Lô Xiên 2 (A, B) nổ cùng nhau nhiều nhất trong N kỳ gần đây
        """
        if not self.draws:
            return []

        pair_counter = Counter()
        target_draws = self.draws[:limit_draws]

        for draw in target_draws:
            # Lấy tập hợp các số duy nhất xuất hiện trong kỳ đó (loại bỏ trùng lặp nếu về 2 nháy)
            unique_numbers = sorted(list(set(self._extract_2digit_numbers(draw))))
            # Tạo tất cả các tổ hợp 2 số (Lô Xiên 2)
            pairs = combinations(unique_numbers, 2)
            pair_counter.update(pairs)

        # Trả về Top K cặp xuất hiện nhiều nhất
        return pair_counter.most_common(top_k)
