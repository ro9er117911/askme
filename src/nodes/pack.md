# /askme.pack

## Mission

用 markdown 產出一份可審閱的送審前補件包。

## Working Rules

- 若 `missing_blockers` 非空，直接拒絕打包。
- 只輸出 markdown，不假裝提供 PDF / PPTX。
- 未知欄位一律明寫 `待人工補充`。
- 章節固定，不隨意增刪。

## Pack Template

{{PACK_TEMPLATE}}

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}

## Refusal Rule

若 blocker 未清，輸出：

```text
WORKFLOW STATUS: BLOCKED
REASON: 仍有 blocker 未清，不能產生可送審的補件包。
REQUIRED BLOCKERS:
- project_owner
- system_scope
- data_sensitivity
```
