#!/usr/bin/env python3
from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
ASKME_DIR = REPO_ROOT / ".agents" / "skills" / "askme"
SRC_DIR = ASKME_DIR / "src"


def load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml is not None:
        return yaml.safe_load(text)
    return json.loads(text)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def dump_json_yaml(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def code_block(text: str, language: str = "") -> str:
    fence = f"```{language}".rstrip()
    return f"{fence}\n{text.strip()}\n```"


def neutralize_template_vars(text: str) -> str:
    return text.replace("{{", "<").replace("}}", ">")


def format_description_block(description: str) -> str:
    return "\n".join(f"  {line}" for line in textwrap.wrap(description, width=72))


def build_frontmatter(config: dict[str, Any], node_id: str) -> str:
    package = config["package"]
    node = config["nodes"][node_id]
    metadata = {
        "author": package["author"],
        "language": package["language"],
        "category": package["category"],
        "short-description": node["short_description"],
        "openclaw": {"emoji": node["emoji"]},
    }
    description = format_description_block(node["description"])
    return (
        "---\n"
        f"name: {node['skill_name']}\n"
        f"version: {package['version']}\n"
        "user-invocable: true\n"
        "description: |\n"
        f"{description}\n"
        f"metadata: {json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))}\n"
        "---\n\n"
    )


def render_profile_rules(profile: dict[str, Any], threshold: float) -> str:
    include_any = "、".join(profile["routing_clues"]["include_any"])
    exclude_any = "、".join(profile["routing_clues"]["exclude_any"])
    return "\n".join(
        [
            f"- 命中任一 include clue：{include_any}",
            f"- 命中任一 exclude clue：{exclude_any}",
            f"- 有足夠 include clue 且未命中 exclude clue 時，才可判定為 `{profile['profile']}`。",
            f"- 若線索不足，`confidence` 不得高於 {threshold:.2f}，並應回 `NEEDS_CONTEXT`。",
        ]
    )


def render_required_fields(profile: dict[str, Any]) -> str:
    return "\n".join(
        f"- `{field}`：{profile['field_guidance'][field]}" for field in profile["required_fields"]
    )


def render_named_field_group(title: str, fields: list[str], guidance: dict[str, str]) -> str:
    lines = [f"## {title}", ""]
    lines.extend(f"- `{field}`：{guidance.get(field, '待補說明')}" for field in fields)
    return "\n".join(lines)


def render_case_packet_fields(contract: dict[str, Any]) -> str:
    return "\n".join(
        f"- `{field}`：{meta['description']}" for field, meta in contract["fields"].items()
    )


def render_read_write_matrix(config: dict[str, Any], contract: dict[str, Any]) -> str:
    header = "| Node | Reads | Writes | BLOCKED | NEEDS_CONTEXT |"
    divider = "|------|-------|--------|---------|---------------|"
    rows = [header, divider]
    for node_id, meta in config["nodes"].items():
        node = contract["nodes"][node_id]
        reads = "<br>".join(node["reads"]) or "—"
        writes = "<br>".join(node["writes"]) or "—"
        blocked = "<br>".join(node["blocked_when"]) or "—"
        needs = "<br>".join(node["needs_context_when"]) or "—"
        rows.append(f"| `{meta['command']}` | {reads} | {writes} | {blocked} | {needs} |")
    return "\n".join(rows)


def render_node_io(config: dict[str, Any], contract: dict[str, Any], node_id: str) -> str:
    node_meta = config["nodes"][node_id]
    node = contract["nodes"][node_id]
    sections = [
        f"- Command: `{node_meta['command']}`",
        f"- Reads: {', '.join(node['reads']) if node['reads'] else '—'}",
        f"- Writes: {', '.join(node['writes']) if node['writes'] else '—'}",
        f"- Minimum outputs: {', '.join(node['minimum_outputs'])}",
        f"- BLOCKED when: {', '.join(node['blocked_when']) if node['blocked_when'] else '—'}",
        f"- NEEDS_CONTEXT when: {', '.join(node['needs_context_when']) if node['needs_context_when'] else '—'}",
    ]
    return "\n".join(sections)


def render_question_bank(question_bank: dict[str, Any]) -> str:
    chunks: list[str] = []
    for category in question_bank["categories"]:
        chunks.append(f"### {category['label']}")
        for idx, question in enumerate(category["questions"], start=1):
            fills = ", ".join(question["fills"])
            chunks.append(f"{idx}. [{question['priority']}] {question['prompt']}")
            chunks.append(f"   - fills: `{fills}`")
        chunks.append("")
    return "\n".join(chunks).strip()


def render_impact_axes(profile: dict[str, Any]) -> str:
    axes = profile["impact_axes"]
    return "\n".join(
        [
            "### Roles",
            bullet_list(axes["roles"]),
            "",
            "### Systems",
            bullet_list(axes["systems"]),
            "",
            "### Processes",
            bullet_list(axes["processes"]),
        ]
    )


def render_pack_template(template_text: str, profile: dict[str, Any]) -> str:
    sections = "\n".join(f"- `{section}`" for section in profile["pack"]["sections"])
    return (
        "固定章節順序：\n"
        f"{sections}\n\n"
        "模板：\n\n"
        f"{code_block(neutralize_template_vars(template_text), 'md')}"
    )


def render_regulation_map(regulations: dict[str, Any]) -> str:
    lines = ["### Baseline", ""]
    for item in regulations["baseline"]:
        lines.append(f"- `{item['name']}`：{item['notes']}")
    lines.extend(["", "### Conditional Rules", ""])
    for rule in regulations["conditional_rules"]:
        lines.append(f"- When: {rule['when']}")
        lines.append(f"  - Regulations: {'、'.join(rule['regulations'])}")
        lines.append(f"  - Review flags: {'、'.join(rule['review_flags'])}")
    lines.extend(["", "### Required Risk Fields", "", bullet_list(regulations["required_risk_fields"])])
    return "\n".join(lines)


def render_route_preview_template(template_text: str) -> str:
    return code_block(neutralize_template_vars(template_text), "md")


def render_fallback_rules(contract: dict[str, Any]) -> str:
    return bullet_list(contract["fallback_rules"])


def replace_placeholders(
    text: str,
    config: dict[str, Any],
    contract: dict[str, Any],
    profile: dict[str, Any],
    question_bank: dict[str, Any],
    regulations: dict[str, Any],
    route_preview_template: str,
    pack_template: str,
    node_id: str,
) -> str:
    replacements = {
        "{{PROFILE_RULES}}": render_profile_rules(profile, config["routes"]["auto"]["confidence_threshold"]),
        "{{REQUIRED_FIELDS}}": render_required_fields(profile),
        "{{BLOCKER_FIELDS}}": render_named_field_group("Blocker Fields", profile["blocker_fields"], profile["field_guidance"]),
        "{{FOLLOWUP_FIELDS}}": render_named_field_group("Follow-up Fields", profile["followup_fields"], profile["field_guidance"]),
        "{{COMMON_FALLBACK_RULES}}": render_fallback_rules(contract),
        "{{CASE_PACKET_FIELDS}}": render_case_packet_fields(contract),
        "{{READ_WRITE_MATRIX}}": render_read_write_matrix(config, contract),
        "{{NODE_IO}}": render_node_io(config, contract, node_id),
        "{{QUESTION_BANK}}": render_question_bank(question_bank),
        "{{IMPACT_AXES}}": render_impact_axes(profile),
        "{{PACK_TEMPLATE}}": render_pack_template(pack_template, profile),
        "{{REGULATION_MAP}}": render_regulation_map(regulations),
        "{{ROUTE_PREVIEW_TEMPLATE}}": render_route_preview_template(route_preview_template),
    }
    for placeholder, rendered in replacements.items():
        text = text.replace(placeholder, rendered)
    unresolved = [token for token in text.split() if token.startswith("{{") and token.endswith("}}")]
    if unresolved:
        raise ValueError(f"Unresolved placeholders in {node_id}: {unresolved}")
    return text.strip() + "\n"


def build_vscode_prompt(node_meta: dict[str, Any], body: str) -> str:
    intro = (
        "<!-- AUTO-GENERATED by scripts/generate_askme.py. Edit source under "
        ".agents/skills/askme/src/. -->\n\n"
        f"# Standalone Prompt: {node_meta['command']}\n\n"
        "Use this file as a self-contained prompt for VS Code agents such as Cline "
        "or Copilot Chat. It must not assume access to any other askme files at "
        "runtime.\n\n"
    )
    return intro + body


def write_file(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def mirror_source_assets(target_root: Path) -> None:
    mirrors = [
        (SRC_DIR / "config.yaml", target_root / "config.yaml"),
        (SRC_DIR / "contracts" / "case-packet.yaml", target_root / "contracts" / "case-packet.yaml"),
        (SRC_DIR / "profiles" / "bank-aigov-inherent-risk.yaml", target_root / "profiles" / "bank-aigov-inherent-risk.yaml"),
        (SRC_DIR / "question-bank" / "bank-aigov.yaml", target_root / "question-bank" / "bank-aigov.yaml"),
        (SRC_DIR / "regulations" / "bank-aigov.yaml", target_root / "regulations" / "bank-aigov.yaml"),
        (SRC_DIR / "templates" / "route-preview.md", target_root / "templates" / "route-preview.md"),
        (SRC_DIR / "templates" / "pack.md", target_root / "templates" / "pack.md"),
    ]
    for source, target in mirrors:
        write_file(target, source.read_text(encoding="utf-8"))


def build_all(target_root: Path | None = None) -> Path:
    target_root = target_root or ASKME_DIR
    config = load_structured(SRC_DIR / "config.yaml")
    contract = load_structured(SRC_DIR / "contracts" / "case-packet.yaml")
    profile = load_structured(SRC_DIR / "profiles" / "bank-aigov-inherent-risk.yaml")
    question_bank = load_structured(SRC_DIR / "question-bank" / "bank-aigov.yaml")
    regulations = load_structured(SRC_DIR / "regulations" / "bank-aigov.yaml")
    route_preview_template = load_text(SRC_DIR / "templates" / "route-preview.md")
    pack_template = load_text(SRC_DIR / "templates" / "pack.md")

    mirror_source_assets(target_root)

    for node_id, node_meta in config["nodes"].items():
        source_body = load_text(SRC_DIR / "nodes" / f"{node_id}.md")
        compiled_body = replace_placeholders(
            source_body,
            config=config,
            contract=contract,
            profile=profile,
            question_bank=question_bank,
            regulations=regulations,
            route_preview_template=route_preview_template,
            pack_template=pack_template,
            node_id=node_id,
        )

        runtime_content = (
            "<!-- AUTO-GENERATED by scripts/generate_askme.py. Edit source under "
            ".agents/skills/askme/src/. -->\n"
            + build_frontmatter(config, node_id)
            + compiled_body
        )
        vscode_content = build_vscode_prompt(node_meta, compiled_body)

        write_file(target_root / node_meta["runtime_path"], runtime_content)
        write_file(target_root / node_meta["codex_path"], runtime_content)
        write_file(target_root / node_meta["vscode_path"], vscode_content)

    return target_root


if __name__ == "__main__":
    build_all()
