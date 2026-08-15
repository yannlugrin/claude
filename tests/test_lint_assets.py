"""Tests for scripts/lint-assets.py — the frontmatter gate.

What it guards is a silent failure: a skill whose frontmatter will not parse
does not error at load time, it simply never loads. So the cases that matter
are the malformed ones, and the rule that a supporting file inside a skill
directory is not held to the entrypoint's contract.
"""

import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "lint_assets",
    Path(__file__).resolve().parent.parent / "scripts" / "lint-assets.py",
)
lint_assets = importlib.util.module_from_spec(_SPEC)
sys.modules["lint_assets"] = lint_assets
_SPEC.loader.exec_module(lint_assets)


class TestParseFrontmatter(unittest.TestCase):
    def test_no_frontmatter_is_not_an_error(self):
        data, error = lint_assets.parse_frontmatter("# just a document\n")
        self.assertIsNone(data)
        self.assertIsNone(error)

    def test_a_closed_block_parses(self):
        data, error = lint_assets.parse_frontmatter(
            "---\nname: x\n---\nbody\n"
        )
        self.assertEqual(data, {"name": "x"})
        self.assertIsNone(error)

    def test_an_unclosed_block_is_an_error(self):
        _, error = lint_assets.parse_frontmatter("---\nname: x\nbody\n")
        self.assertIn("never closed", error)

    def test_invalid_yaml_is_an_error(self):
        _, error = lint_assets.parse_frontmatter("---\nname: [unclosed\n---\n")
        self.assertIn("invalid YAML", error)

    def test_a_non_mapping_is_an_error(self):
        _, error = lint_assets.parse_frontmatter("---\n- a\n- b\n---\n")
        self.assertIn("not a YAML mapping", error)


class CheckFixture(unittest.TestCase):
    """`check` reads from disk and keys on the path, so give it real files."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        self._cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(lambda: os.chdir(self._cwd))
        # The script keys on where a file sits in *this* repository, so the
        # fixture directory has to stand in for the repository root.
        self._real_root = lint_assets.REPO_ROOT
        lint_assets.REPO_ROOT = self.root
        self.addCleanup(self._restore_root)

    def _restore_root(self) -> None:
        lint_assets.REPO_ROOT = self._real_root

    def write(self, relative: str, text: str) -> Path:
        path = Path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path


class TestSkills(CheckFixture):
    def test_a_well_formed_skill_passes(self):
        path = self.write(
            "skills/demo/SKILL.md", "---\ndescription: does a thing\n---\n"
        )
        self.assertEqual(lint_assets.check(path), [])

    def test_missing_frontmatter_is_reported(self):
        path = self.write("skills/demo/SKILL.md", "no frontmatter here\n")
        self.assertIn("missing frontmatter", lint_assets.check(path)[0])

    def test_an_empty_description_is_reported(self):
        path = self.write(
            "skills/demo/SKILL.md", "---\ndescription: '   '\n---\n"
        )
        self.assertIn("non-empty `description`", lint_assets.check(path)[0])

    def test_a_name_disagreeing_with_the_directory_is_reported(self):
        path = self.write(
            "skills/demo/SKILL.md", "---\nname: other\ndescription: x\n---\n"
        )
        self.assertIn("does not match directory", lint_assets.check(path)[0])

    def test_a_matching_name_is_accepted(self):
        path = self.write(
            "skills/demo/SKILL.md", "---\nname: demo\ndescription: x\n---\n"
        )
        self.assertEqual(lint_assets.check(path), [])

    def test_a_supporting_file_is_not_held_to_the_entrypoint_contract(self):
        self.write("skills/demo/SKILL.md", "---\ndescription: x\n---\n")
        path = self.write(
            "skills/demo/references/notes.md", "no frontmatter\n"
        )
        self.assertEqual(lint_assets.check(path), [])

    def test_a_supporting_file_with_broken_frontmatter_is_still_reported(self):
        self.write("skills/demo/SKILL.md", "---\ndescription: x\n---\n")
        path = self.write(
            "skills/demo/references/notes.md", "---\nname: [oops\n---\n"
        )
        self.assertIn("invalid YAML", lint_assets.check(path)[0])


class TestSkillDirectories(CheckFixture):
    def test_a_directory_without_an_entrypoint_is_reported(self):
        path = self.write("skills/orphan/references/notes.md", "notes\n")
        self.assertIn("has no SKILL.md", lint_assets.check(path)[0])

    def test_a_directory_with_one_is_accepted(self):
        self.write("skills/demo/SKILL.md", "---\ndescription: x\n---\n")
        path = self.write("skills/demo/references/notes.md", "notes\n")
        self.assertEqual(lint_assets.check(path), [])


class TestInertSkillKeys(CheckFixture):
    """Keys that look like enforcement and are not — the failure is silence."""

    def test_allowed_tools_is_reported(self):
        path = self.write(
            "skills/demo/SKILL.md",
            "---\ndescription: x\nallowed-tools:\n  - Read\n---\n",
        )
        self.assertIn("`allowed-tools`", lint_assets.check(path)[0])

    def test_disallowed_tools_is_reported(self):
        path = self.write(
            "skills/demo/SKILL.md",
            "---\ndescription: x\ndisallowed-tools: Edit\n---\n",
        )
        self.assertIn("stranding", lint_assets.check(path)[0])

    def test_when_to_use_is_reported(self):
        path = self.write(
            "skills/demo/SKILL.md",
            "---\ndescription: x\nwhen_to_use: sometimes\n---\n",
        )
        self.assertIn("`when_to_use`", lint_assets.check(path)[0])

    def test_an_agent_may_still_declare_tools(self):
        """`tools:` binds for agents; only skills are lied to."""
        path = self.write(
            "agents/helper.md",
            "---\nname: helper\ndescription: x\ntools: Read\n---\n",
        )
        self.assertEqual(lint_assets.check(path), [])


class TestOutsideTheRepository(CheckFixture):
    def test_a_path_outside_the_repository_is_refused_not_ignored(self):
        outside = Path(self._real_root) / "README.md"
        self.assertIn("outside the repository", lint_assets.check(outside)[0])

    def test_a_file_in_no_asset_directory_has_no_rules(self):
        path = self.write("notes/scratch.md", "no frontmatter\n")
        self.assertEqual(lint_assets.check(path), [])


class TestAgents(CheckFixture):
    def test_a_well_formed_agent_passes(self):
        path = self.write(
            "agents/helper.md", "---\nname: helper\ndescription: x\n---\n"
        )
        self.assertEqual(lint_assets.check(path), [])

    def test_missing_frontmatter_is_reported(self):
        path = self.write("agents/helper.md", "system prompt only\n")
        self.assertIn("missing frontmatter", lint_assets.check(path)[0])

    def test_each_missing_field_is_reported(self):
        path = self.write("agents/helper.md", "---\nname: ''\n---\n")
        errors = " ".join(lint_assets.check(path))
        self.assertIn("`name`", errors)
        self.assertIn("`description`", errors)


class TestCommands(CheckFixture):
    def test_frontmatter_is_optional(self):
        path = self.write("commands/old.md", "just a prompt\n")
        self.assertEqual(lint_assets.check(path), [])

    def test_but_must_parse_when_present(self):
        path = self.write("commands/old.md", "---\nbad: [\n---\n")
        self.assertIn("invalid YAML", lint_assets.check(path)[0])


class TestMain(CheckFixture):
    def test_exit_status_is_one_when_a_file_fails(self):
        self.write("agents/helper.md", "no frontmatter\n")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status = lint_assets.main(["agents/helper.md"])
        self.assertEqual(status, 1)
        self.assertIn("missing frontmatter", out.getvalue())

    def test_exit_status_is_zero_when_every_file_passes(self):
        self.write(
            "agents/helper.md", "---\nname: helper\ndescription: x\n---\n"
        )
        self.assertEqual(lint_assets.main(["agents/helper.md"]), 0)


if __name__ == "__main__":
    unittest.main()
