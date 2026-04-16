# /askme.how

## Mission

把「系統導入前後的作業流程差異」整理成文字對比，對應架審文件的「應用情境」區塊。

## Core Questions

- 現在的作業流程是什麼？誰做什麼、用什麼系統？
- 導入後，流程哪裡改變了？（新增步驟 / 移除步驟 / 自動化哪段）
- 發動者是誰？留存在哪裡？

## Working Rules

- 先 Scan：讀取 `case_packet`，自動填入已知的流程描述片段。
- 再 Show：列出已捕獲 ✅ 與待補充 ❌。
- 只輸出文字描述，不繪製流程圖。
- 若流程仍不清楚，只問「發動點」和「主要差異」這兩個問題。
- 允許使用者回答「先跳過」並標為 `⏭ 待補`。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

填入 `case_packet` 的 `how_summary`，格式如下：

```text
應用情境

發動者：[系統/角色]　留存：[資料庫/系統]

原本業務流程：
[步驟 A] → [步驟 B] → [步驟 C（人工）]

新業務流程：
[步驟 A] → [新步驟 X（AI 自動）] → [步驟 B] → [步驟 C（簡化）]

主要差異：
• [差異說明一]
• [差異說明二]

⚠️ 建議補充：一張「舊流程 vs 新流程」對比圖是審查委員最直觀的理解入口。
```

若輸入不足以描述任何流程，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 無法從現有輸入判定業務流程轉變。
RECOMMENDATION: 請補充「現在怎麼做、導入後哪裡不同」的簡短說明。
```
