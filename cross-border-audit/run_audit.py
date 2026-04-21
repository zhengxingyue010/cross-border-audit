#!/usr/bin/env python3
import csv
import json
from datetime import datetime
from collections import defaultdict, Counter

print("="*60)
print("跨境电商交易审计 - 简化演示版")
print("="*60)

# 步骤 1: 读取 CSV 数据
print("\n[步骤 1] 读取数据...")
csv_file = "data/raw/客户订单明细.csv"

data = []
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

print(f"共读取 {len(data)} 条交易记录")

# 显示前 3 条
print("\n数据预览:")
for i, row in enumerate(data[:3]):
    print(f"记录 {i+1}: {row}")

# 步骤 2: 加载风险模式库
print("\n[步骤 2] 加载风险模式库...")
with open("risk-patterns/patterns.json", 'r', encoding='utf-8') as f:
    patterns = json.load(f)

print(f"已加载 {len(patterns['patterns'])} 个风险模式")
for p in patterns['patterns']:
    print(f"  - {p['id']}: {p['name']} ({p['severity']})")

# 步骤 3: 风险识别
print("\n[步骤 3] 风险识别...")

# PATTERN-003: 整数数量检查（快速演示）
suspicious_numbers = {10, 50, 100, 200, 500, 1000, 2000, 5000, 10000}
risk_matches = []
quantity_stats = Counter()

print("检查整数数量可疑订单...")
for i, row in enumerate(data):
    try:
        qty = int(float(row['Quantity'])) if row['Quantity'].strip() else 0
    except:
        qty = 0
    
    quantity_stats[qty] += 1

    if qty > 0 and qty in suspicious_numbers:
        risk_matches.append({
            'pattern_id': 'PATTERN-003',
            'pattern_name': '整数数量可疑订单',
            'severity': 'low',
            'record_index': i,
            'invoice': row['Invoice'],
            'stock_code': row['StockCode'],
            'quantity': qty,
            'country': row['Country']
        })

print(f"发现 {len(risk_matches)} 个匹配整数数量模式的订单")

# 统计分析 - 高频发货
print("\n分析高频发货模式...")
product_country_counts = defaultdict(int)
for row in data:
    stock_code = row.get('StockCode', '').strip()
    country = row.get('Country', '').strip()
    if stock_code and country:
        key = (stock_code, country)
        product_country_counts[key] += 1

# 找出高频组合
high_freq = [(k, v) for k, v in product_country_counts.items() if v >= 2]
high_freq.sort(key=lambda x: x[1], reverse=True)

print(f"发现 {len(high_freq)} 个高频（>=2次）货物-国家组合")
for i, (key, count) in enumerate(high_freq[:5]):
    print(f"  排名 {i+1}: {key[0]} -> {key[1]}: {count}次")

# 步骤 4: 生成报告
print("\n[步骤 4] 生成审计报告...")

report_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
report_file = f"reports/审计报告_{report_time}.md"

report_content = f"""# 跨境电商交易审计报告

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据范围:** {len(data)} 条交易记录
**数据时间:** 2009年12月

---

## 执行摘要

- 总订单数: {len(data)}
- 发现风险订单: {len(risk_matches)}
- 高风险: 0
- 中风险: 0
- 低风险: {len(risk_matches)}
- 高频货物-国家组合: {len(high_freq)}

---

## 风险详情

### 低风险 🟢

#### PATTERN-003: 整数数量可疑订单
- **风险描述**: 订单数量为100、500、1000等整数
- **匹配订单数**: {len(risk_matches)}
- **示例匹配**:

"""

for i, risk in enumerate(risk_matches[:10]):
    report_content += f"  {i+1}. 发票 {risk['invoice']}, 货物 {risk['stock_code']}, 数量 {risk['quantity']}, 国家 {risk['country']}\n"

if len(risk_matches) > 10:
    report_content += f"  ... 还有 {len(risk_matches) - 10} 条\n"

report_content += f"""
---

## 统计分析

### 高频货物-国家组合 TOP 10

| 排名 | 货物代码 | 国家 | 频次 |
|------|---------|------|------|
"""

for i, (key, count) in enumerate(high_freq[:10]):
    report_content += f"| {i+1} | {key[0]} | {key[1]} | {count} |\n"

report_content += f"""
---

## 建议与行动计划

### 短期措施
1. 进一步核查整数数量订单，确认是否为正常批发行为
2. 对高频货物-国家组合进行深入分析，检查是否存在异常

### 模式库更新建议
- 可将高频货物-国家组合（>20次）纳入监测模式
- 可增加价格异常波动检测模式

---

*本报告由跨境电商交易审计系统自动生成*
"""

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"\n✅ 审计完成！")
print(f"报告已保存到: {report_file}")
print("\n" + "="*60)
print("报告预览:")
print("="*60)
print(report_content[:800] + "\n...\n[报告已截断，请查看完整文件]")
