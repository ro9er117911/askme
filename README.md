# askme

`askme` is now maintained as a compiled prompt package.

Source of truth lives under `src/`. Generated artifacts are written to:

- runtime Codex skills:
  - `SKILL.md`
  - `<node>/SKILL.md`
- distribution bundles:
  - `dist/codex/*.md`
  - `dist/vscode/*.prompt.md`
- compatibility mirrors for shared assets:
  - `config.yaml`
  - `contracts/*.yaml`
  - `profiles/*.yaml`
  - `question-bank/*.yaml`
  - `regulations/*.yaml`
  - `templates/*.md`

## Layout

```text
askme/
├─ src/
│  ├─ config.yaml
│  ├─ contracts/
│  ├─ nodes/
│  ├─ profiles/
│  ├─ question-bank/
│  ├─ regulations/
│  └─ templates/
├─ dist/
│  ├─ codex/
│  └─ vscode/
├─ tests/
└─ SKILL.md
```

## Regenerate

```bash
python3 scripts/generate_askme.py
```

## Cline (VS Code) 安裝指南 (Windows)

對於使用 **Cline** 或 **Roo-Code** 的 Windows 使用者，請依照以下步驟啟用原生的 Slash (`/`) 指令：

1.  **建立指令目錄**：
    確保您的專案根目錄下存在以下路徑（若無請手動建立）：
    `C:\Users\您的使用者\Desktop\專案名稱\.clinerules\workflows`

2.  **同步指令檔**：
    *   **方法 A (自動)**：在終端機執行 `python scripts/generate_askme.py`，腳本會自動將指令同步至 `.clinerules/workflows`。
    *   **方法 B (手動)**：將 `dist/vscode/askme.prompt.md` 複製到 `.clinerules/workflows/askme.md`。

3.  **啟用指令**：
    在 Cline 的輸入框中輸入 **`/`**，即可在選單中看到 `/askme`、`/askme.intake` 等指令。

> [!TIP]
> 如果輸入 `/` 後沒看到指令，請確認 `.clinerules` 資料夾沒有被 Windows 系統完全隱藏，或點擊 Cline 面板上方的 **Workflows** 標籤重新整理。


## Test

```bash
python3 -m unittest discover -s .agents/skills/askme/tests
```

## Notes

- Source `.yaml` files are written as JSON-compatible YAML so the generator can run with Python stdlib only.
- Runtime skills and VS Code prompt packs are intentionally self-contained. They must not require any file outside the `askme` package at execution time.
