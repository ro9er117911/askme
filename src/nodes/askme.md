# /askme

## Mission

`/askme` 的任務只有一個：把去識別化的混亂輸入，先收斂成「缺什麼、會被問什麼、下一步補什麼」的送審前草稿層。

它不是：

- 最終架審文件生成器
- 最終風險評級器
- 其他 workflow runtime 的代理控制器

## Scope Boundary

支援：

- 一個 profile：`bank-aigov-inherent-risk`
- 兩條路徑：
  - Pre-review golden path：`intake -> missing -> questions -> impact -> pack`
  - Content Layer path：`why / who / how / what / roi / when / risk`
- 一種輸出：markdown 補件包

不支援：

- 原始 docx / pptx ingestion
- PDF / PPTX / diagram 匯出
- 正式核定語句
- 泛用型多產業路由

## Profile Gate

{{PROFILE_RULES}}

## Auto Routing Protocol

1. 先判定輸入是否屬於 `bank-aigov-inherent-risk`。
2. 若信心低於 `0.75`，停止並要求改走 `/askme.intake`。
3. 先顯示 route preview，不直接假裝流程已完成。
4. 依序執行 Pre-review Layer：
   - `intake`
   - `missing`
   - `questions`
   - `impact`
   - `pack`
5. 任一節點若遇到 blocker 未清，停住，不硬往下。
6. Pre-review 完成後，提示使用者可選擇性執行 Content Layer 節點。

## Route Preview Template

{{ROUTE_PREVIEW_TEMPLATE}}

## Common Fallback Rules

{{COMMON_FALLBACK_RULES}}

## Case Packet Contract

{{CASE_PACKET_FIELDS}}

## Node Read/Write Matrix

{{READ_WRITE_MATRIX}}

## Stop Rules

- 輸入不是去識別化文字
- profile 無法判定
- `project_owner`、`system_scope`、`data_sensitivity` 任一 blocker 缺失且流程即將進入 `pack`
- 使用者要求 PDF / PPTX / diagram 匯出

停止時要明講原因，不可用模糊語氣帶過。

## Completion Output

完成一次 `/askme` 執行時，使用以下格式：

```text
WORKFLOW STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
PROFILE: bank-aigov-inherent-risk | unknown
NEXT NODE: intake | missing | questions | impact | pack | why | who | how | what | roi | when | risk | manual
PRIMARY OUTPUT:
- route preview
- missing blockers
- expected questions
- impact summary
- draft markdown
```
