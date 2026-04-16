# /askme.missing

## Mission

把 `case_packet` 中尚未補齊的資訊切成：

- `missing_blockers`
- `followups`

## Field Groups

{{BLOCKER_FIELDS}}

{{FOLLOWUP_FIELDS}}

## Working Rules

- 先比對 `required_fields` 的完整度。
- `project_owner`、`system_scope`、`data_sensitivity` 任何一個缺失，都列為 blocker。
- 只列缺口，不在此節點補答案。
- 若所有 blocker 已清，但 follow-up 仍有缺口，允許流程進到 `questions`。
- 若沒有缺口，也要明示 `missing_blockers: []`，不要留白。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}
