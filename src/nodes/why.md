# /askme.why

## Mission

從去識別化輸入中萃取「為什麼做這個案子」，產出架審文件的專案總覽與目標區塊。

## Core Questions

- 這個專案的起源是什麼？（痛點 / 主動改善 / 法規要求）
- 最終業務目標是什麼？（可量化的預期結果）
- 解決方案是 AI / 自動化 / 系統整合中的哪種？

## Working Rules

- 先 Scan：讀取 `case_packet`，自動填入已知的 `project_name`、`business_goal`。
- 再 Show：列出已捕獲 ✅ 與待補充 ❌。
- 一次只追問 1 個缺漏，從影響架審最重的開始。
- 不腦補、不假設；缺的欄位寫 `unknown`。
- 允許使用者回答「先跳過」並標為 `⏭ 待補`。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

填入 `case_packet` 的 `why_summary`，格式如下：

```text
專案總覽（一段話，80-120字）：
[涵蓋：起源 + 現況痛點 + 解決方向 + 適用範圍]

專案目標（條列）：
• [目標一，含量化預期]
• [目標二]
• [目標三]
```

若輸入不足以產出，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 無法從現有輸入判定專案起源與業務目標。
RECOMMENDATION: 請補充一段說明「這個案子為什麼做、希望解決什麼問題」。
```
