# /askme.impact

## Mission

把前面收集到的事實收斂成三種 impact：

- 影響角色
- 影響系統
- 影響流程

## Impact Axes

{{IMPACT_AXES}}

## Working Rules

- 只用 `case_packet` 與目前 profile 的 impact 軸線。
- 不做正式風險分數。
- 不做 go / no-go 決策。
- 若某一軸缺資料，可以寫 `待人工補充`。
- 若系統邊界仍不清楚，回頭補 `questions` 或 `/askme.what`。

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Output Contract

`impact_summary` 固定要有三個區塊：

- `roles`
- `systems`
- `processes`

最後補一句：

`這份 impact summary 用於送審前對焦，不代表最終治理結論。`

若系統邊界與流程影響都無法識別，輸出：

```text
WORKFLOW STATUS: NEEDS_CONTEXT
REASON: 無法從現有輸入穩定整理出受影響角色、系統與流程。
RECOMMENDATION: 請先補充本案會碰到哪些系統、誰會用、流程哪裡改變。
```
