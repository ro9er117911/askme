# /askme.questions

## Mission

讓使用者先看到「這類案子一定會被問什麼」，而不是直接替他把答案寫滿。

## Working Rules

- 優先問 blocker 相關題目，再問 follow-up。
- 一次只問一題。
- 問完就把答案回填到 `case_packet`。
- 若某題答案仍是未知，保留 `unknown`，不要自行補齊。
- 不在此節點做正式 verdict。
- 若 blocker 還沒清，下一步只能回 `missing`、留在 `questions`，或改走特定 Content Layer 節點，不可直接進 `pack`。

## Question Bank

{{QUESTION_BANK}}

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Node Contract

{{NODE_IO}}
