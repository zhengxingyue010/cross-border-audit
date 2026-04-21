#!/usr/bin/env python3
import csv
from collections import defaultdict

csv_file = "data/raw/客户订单明细.csv"

print("快速统计...")
product_country_counts = defaultdict(int)
all_stock_codes = set()
all_countries = set()

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        stock_code = row.get('StockCode', '').strip()
        country = row.get('Country', '').strip()
        
        if stock_code:
            all_stock_codes.add(stock_code)
        if country:
            all_countries.add(country)
            
        if stock_code and country:
            key = (stock_code, country)
            product_country_counts[key] += 1

print(f"唯一货物代码: {len(all_stock_codes)}")
print(f"唯一国家: {len(all_countries)}")
print(f"国家列表: {sorted(all_countries)}")

# 找出前20的组合
sorted_items = sorted(product_country_counts.items(), key=lambda x: x[1], reverse=True)
print(f"\n前20高频货物-国家组合:")
for i, ((stock, country), count) in enumerate(sorted_items[:20]):
    print(f"{i+1}. {stock} -> {country}: {count}次")
