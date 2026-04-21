# 跨境电商交易审计系统

跨境电商交易订单的风险审计与刷单风险自动识别系统，具备自动学习能力的风险模式库。

## 功能特性

- **数据预处理**：自动清洗和标准化 CSV 交易数据
- **风险模式识别**：基于已知风险模式识别可疑交易
- **自动学习**：发现新风险模式并更新模式库
- **审计报告生成**：生成详细的审计报告和改进建议

## 风险检测能力

| 风险模式 | 描述 | 严重程度 |
|---------|------|---------|
| PATTERN-001 | 新注册买家大额订单 | 高 |
| PATTERN-002 | 重复收货地址/电话 | 中 |
| PATTERN-003 | 整数数量可疑订单 | 低 |
| 自定义模式 | 持续学习和扩展 | 可变 |

## 项目结构
此库仅展示openclaw框架工作区中项目文件cross-border-audit文件

```
cross-border-audit/
├── data/                          # 数据目录
│   └── raw/                       # 原始 CSV 数据文件
├── reports/                       # 生成的审计报告
├── risk-patterns/                 # 风险模式库（长期记忆）
│   ├── patterns.json              # 结构化风险模式
│   └── lessons-learned.md         # 经验教训总结
├── skills/                        # 核心功能模块
│   ├── csv-preprocessor/          # CSV 预处理
│   ├── risk-detector/             # 风险识别
│   └── report-generator/          # 报告生成
├── run_audit.py                   # 主审计程序
├── quick_stats.py                 # 快速统计分析
├── convert_excel.py               # Excel 转换工具
└── WORKFLOW.md                    # 详细工作流文档
```

## 快速开始

### 1. 准备数据

将交易数据 CSV 文件放入 `data/raw/` 目录：

```csv
Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country
536365,85123A,WHITE HANGING...,6,12/1/2009 8:26,2.55,17850,United Kingdom
```

### 2. 运行审计

```bash
python run_audit.py
```

### 3. 查看报告

审计报告将生成在 `reports/` 目录，文件名格式：`审计报告_YYYY-MM-DD_HHMMSS.md`

## 使用示例

```bash
# 完整审计流程
python run_audit.py

# 快速统计分析
python quick_stats.py

# Excel 转 CSV
python convert_excel.py
```

## 审计流程

```
原始CSV → [CSV预处理] → 清洗后数据 → [风险识别] → 风险标记数据 → [报告生成] → 审计报告
              ↓                              ↓
        清洗报告                      更新风险模式库
```

## 技术栈

- Python 3.x
- 标准库：csv, json, datetime, collections
- 无第三方依赖，开箱即用

## 自定义风险模式

编辑 `risk-patterns/patterns.json` 添加新的风险模式：

```json
{
  "patterns": [
    {
      "id": "PATTERN-004",
      "name": "自定义风险模式",
      "severity": "medium",
      "conditions": [...]
    }
  ]
}
```

## 许可证

MIT License
