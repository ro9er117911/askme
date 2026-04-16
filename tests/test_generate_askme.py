from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
ASKME_DIR = REPO_ROOT / ".agents" / "skills" / "askme"
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate_askme.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_askme", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AskmeGenerationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.askme_out = Path(cls.temp_dir.name) / "askme"
        cls.generator.build_all(target_root=cls.askme_out)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_dist_files_exist_for_all_nodes(self):
        config = self.generator.load_structured(ASKME_DIR / "src" / "config.yaml")
        for node_meta in config["nodes"].values():
            self.assertTrue((self.askme_out / node_meta["runtime_path"]).exists())
            self.assertTrue((self.askme_out / node_meta["codex_path"]).exists())
            self.assertTrue((self.askme_out / node_meta["vscode_path"]).exists())

    def test_generated_runtime_and_dist_are_self_contained(self):
        forbidden = [
            "SDD_kit",
            ".agents/skills/bank-",
            "../",
            "../../",
            "../../../",
            "/askme:diagram-sync",
        ]
        generated_files = list((self.askme_out / "dist" / "codex").glob("*.md"))
        generated_files += list((self.askme_out / "dist" / "vscode").glob("*.md"))
        generated_files += [self.askme_out / "SKILL.md"]
        generated_files += list(self.askme_out.glob("*/SKILL.md"))
        for path in generated_files:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, msg=f"{token} leaked into {path}")

    def test_contract_matrix_covers_all_public_commands(self):
        config = self.generator.load_structured(ASKME_DIR / "src" / "config.yaml")
        contract = self.generator.load_structured(ASKME_DIR / "src" / "contracts" / "case-packet.yaml")
        commands = {meta["command"] for meta in config["nodes"].values()}
        self.assertEqual(commands, set(contract["public_commands"]))
        self.assertEqual(set(config["nodes"].keys()), set(contract["nodes"].keys()))

    def test_questions_prompt_inlines_question_bank(self):
        questions_skill = (self.askme_out / "questions" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("### Business", questions_skill)
        self.assertIn("這次送審前草稿的真正目的", questions_skill)
        self.assertIn("### Compliance", questions_skill)
        self.assertIn("### Audit", questions_skill)

    def test_risk_prompt_inlines_regulation_rules(self):
        risk_skill = (self.askme_out / "risk" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("金融機構運用新興科技作業規範", risk_skill)
        self.assertIn("金融機構作業委託他人處理內部作業制度及程序辦法", risk_skill)
        self.assertIn("data_sensitivity 為 risk 節點的 blocker", risk_skill)

    def test_pack_prompt_keeps_fixed_sections(self):
        pack_skill = (self.askme_out / "pack" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("固定章節順序", pack_skill)
        self.assertIn("`case-summary`", pack_skill)
        self.assertIn("`impact-summary`", pack_skill)
        self.assertIn("WORKFLOW STATUS: BLOCKED", pack_skill)

    def test_main_skill_contains_matrix_and_route_preview(self):
        main_skill = (self.askme_out / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("| Node | Reads | Writes | BLOCKED | NEEDS_CONTEXT |", main_skill)
        self.assertIn("# /askme Route Preview", main_skill)
        self.assertIn("## Case Packet Contract", main_skill)


if __name__ == "__main__":
    unittest.main()
