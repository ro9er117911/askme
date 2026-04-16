# /askme.what

## Mission

整理「這個案子碰哪些系統、資料怎麼流、技術棧是什麼」，對應架審文件的「專案範圍」與「系統架構」區塊。

## Core Questions

- 這個專案牽涉到哪些既有系統？需要新增哪些模組？
- 資料來源是哪裡？以什麼方式串接（API / DB / 排程）？
- 開發語言與框架是什麼？

## Working Rules

- 先 Scan：讀取 `case_packet`，自動填入已知的 `system_scope`。
- 再 Show：列出已捕獲 ✅ 與待補充 ❌。
- IT 窗口若未提供，列為 `⚠️ 待指定`，不腦補。
- API 規格若未說明，標為 `⏭ 待補`，不假設。
- 允許使用者回答「先跳過」並標為 `⏭ 待補`。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

填入 `case_packet` 的 `what_summary`，格式如下：

```text
專案範圍（系統對照表）：

| 序號 | 系統名稱 | IT 窗口 | 本案涉及的異動 |
|------|---------|--------|--------------|
| 1    | [系統]  | [姓名 / ⚠️ 待指定] | [異動說明] |

系統架構摘要：
- 架構模式：[Web API / 排程批次 / 事件驅動]
- 開發語言：[語言 + 版本]
- 模型環境：[框架 + 版本]
- 執行頻率：[即時 / 每週 / 觸發式]
- 資料流向：[來源系統] → [處理層] → [目標系統]

⏭ 待補：
- API 規格文件（Request / Response schema）
- [其他待確認項目]
```

若輸入不足以識別任何系統，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 無法從現有輸入識別牽涉系統或資料流。
RECOMMENDATION: 請補充「這個案子會動到哪些系統、資料從哪裡來、送到哪裡去」。
```
