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

## Test

```bash
python3 -m unittest discover -s .agents/skills/askme/tests
```

## Notes

- Source `.yaml` files are written as JSON-compatible YAML so the generator can run with Python stdlib only.
- Runtime skills and VS Code prompt packs are intentionally self-contained. They must not require any file outside the `askme` package at execution time.
