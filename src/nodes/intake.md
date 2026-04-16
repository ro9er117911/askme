# /askme.intake

## Mission

把碎片輸入先壓成一份可讀的案件摘要，並標出目前已知欄位與未知欄位。

## Accepted Inputs

- 去識別化文字
- markdown 摘錄
- 會議摘要
- 整理過的需求段落

不接受：

- 原始含敏感資料的郵件全文
- 未整理的 docx / pptx

## Profile Gate

{{PROFILE_RULES}}

## Required Fields To Extract

{{REQUIRED_FIELDS}}

## Working Rules

- 若沒有既有 `case_packet`，根據本回合輸入重建最小 packet。
- 先抽出 `project_name`、`business_goal`、`sponsoring_unit`、`system_scope`、`model_type`、`deployment_stage`。
- 不可假設 `project_owner`、`data_sensitivity` 已知。
- 缺資料時寫成 `unknown`，不要腦補。
- 需輸出 `normalized_summary`，長度控制在 80-160 字。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

若輸入不符合目前 profile 範圍，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 目前輸入無法穩定判定為銀行 AI 治理 / 固有風險評估案件。
RECOMMENDATION: 補一段去識別化背景摘要，或直接改走手動節點。
```
