# /askme.roi

## Mission

把「投入多少、產出多少」整理成架審委員可以對焦的量化表格，對應「專案成本」、「資源需求」、「專案效益」三個區塊。

## Core Questions

- 預計投入多少人力？（人月 / 人日）
- 需要什麼硬體資源？（GPU / CPU / Memory / POD 數量）
- 上線後效益是哪幾類？

## Working Rules

- 先 Scan：讀取 `case_packet`，自動填入已知的 `budget_band`。
- 再 Show：列出已捕獲 ✅ 與待補充 ❌。
- 先讓使用者選效益類型，再細填數字。
- 數字不確定時允許填估計值，標 `*估計值`。
- 允許使用者回答「先跳過」並標為 `⏭ 待補`。
- 不代填數字，不腦補人月數。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

填入 `case_packet` 的 `roi_summary`，格式如下：

```text
專案成本：
IT 投入人力：[X] 人月
- [系統/工項]：[X] 人月（含需求確認、系統分析、開發、測試）

資源需求：
| POD Name | POD 數量 | CPU | Memory | GPU | 說明 |
|----------|---------|-----|--------|-----|------|
| [名稱]   | [N]     | [X] core | [X] GB | [規格/不使用] | [框架與用途] |

專案效益：
• 效率提升：[量化描述]  *估計值
• 風險趨避：[量化描述]
• 場景拓展：[說明]

⏭ 待補：[仍未提供量化數字的項目]
```

若輸入完全未提及成本或效益，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 無法從現有輸入估算成本或效益。
RECOMMENDATION: 請補充「大概投入多少人、上線後可以省什麼」的基本說明即可，數字可以是估計值。
```
