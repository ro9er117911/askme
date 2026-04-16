# /askme Route Preview

- Case ID: `{{case_id}}`
- Profile: `{{profile}}`
- Confidence: `{{confidence}}`

## Pre-review Layer（診斷缺口，~50分）

1. `intake`   — 盤點有/缺（8 個必填區塊）
2. `missing`  — Blocker 🔴 / Nice-to-have 🟡 分級
3. `questions`— 預期委員會問題與回填
4. `impact`   — 影響範圍矩陣
5. `pack`     — markdown 補件包

## Content Layer（按維度填充，~70分）

可在 Pre-review 完成後，按需單獨呼叫：

- `/askme.why`  — 專案背景與目標
- `/askme.who`  — 利害關係人與單位
- `/askme.how`  — 業務流程與應用情境
- `/askme.what` — 專案範圍與系統架構
- `/askme.roi`  — 成本、資源、效益量化
- `/askme.when` — 時程與里程碑
- `/askme.risk` — 合規、資安、模型治理

## Current Blockers

{{missing_blockers}}

## Manual Attention Needed

{{manual_attention}}

## Output Boundary

- 只產出 markdown 補件包
- PDF / PPTX / diagram 匯出不在 askme v1 範圍內
