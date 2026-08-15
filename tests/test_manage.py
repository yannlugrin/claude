"""Tests for manage.py — the symlink tool that writes outside this repository.

The behaviour worth pinning down is what it refuses to do. `enable` and
`disable` walk a directory that is usually `~/.claude`, and the promise in
README.md is that they only ever remove symlinks pointing into this repo:
a real file or a foreign symlink at a link path is reported, never deleted.
Every test here runs against a temporary target directory, and a temporary
repository root, so nothing touches the real one.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import manage


class RepoFixture(unittest.TestCase):
    """A throwaway repository and target directory for each test."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.repo = root / "repo"
        self.target = root / "target"
        (self.repo / "skills" / "demo").mkdir(parents=True)
        (self.repo / "skills" / "demo" / "SKILL.md").write_text("---\n---\n")
        (self.repo / "agents").mkdir()
        (self.repo / "agents" / "helper.md").write_text("---\n---\n")
        (self.repo / "agents" / ".hidden.md").write_text("ignored\n")
        self._real_root = manage.REPO_ROOT
        manage.REPO_ROOT = self.repo
        self.addCleanup(self._restore)

    def _restore(self) -> None:
        manage.REPO_ROOT = self._real_root
        self._tmp.cleanup()

    def asset(self, qualified: str) -> manage.Asset:
        kind, _, name = qualified.partition("/")
        return next(a for a in manage.discover() if a.kind == kind and a.name == name)


class TestDiscover(RepoFixture):
    def test_finds_directories_and_files(self):
        found = {a.qualified for a in manage.discover()}
        self.assertEqual(found, {"skills/demo", "agents/helper"})

    def test_skips_dotfiles(self):
        self.assertNotIn("agents/.hidden", {a.qualified for a in manage.discover()})

    def test_name_is_the_stem_for_files_and_the_directory_name_for_directories(self):
        self.assertEqual(self.asset("agents/helper").source.name, "helper.md")
        self.assertEqual(self.asset("skills/demo").source.name, "demo")


class TestState(RepoFixture):
    def test_disabled_when_nothing_is_there(self):
        self.assertEqual(manage.state(self.asset("skills/demo"), self.target), "disabled")

    def test_enabled_when_the_link_points_into_this_repo(self):
        asset = self.asset("skills/demo")
        manage.enable(asset, self.target, force=False)
        self.assertEqual(manage.state(asset, self.target), "enabled")

    def test_conflict_for_a_real_file(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.write_text("someone else's file\n")
        self.assertEqual(manage.state(asset, self.target), "conflict")

    def test_conflict_for_a_symlink_pointing_elsewhere(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.symlink_to(self.repo / "agents" / ".hidden.md")
        self.assertEqual(manage.state(asset, self.target), "conflict")

    def test_conflict_for_a_broken_symlink(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.symlink_to(self.repo / "agents" / "gone.md")
        self.assertEqual(manage.state(asset, self.target), "conflict")


class TestEnable(RepoFixture):
    def test_creates_the_kind_directory_and_the_link(self):
        asset = self.asset("skills/demo")
        message = manage.enable(asset, self.target, force=False)
        link = asset.link_path(self.target)
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), asset.source.resolve())
        self.assertIn("enabled", message)

    def test_is_idempotent(self):
        asset = self.asset("skills/demo")
        manage.enable(asset, self.target, force=False)
        self.assertIn("already enabled", manage.enable(asset, self.target, force=False))

    def test_refuses_a_real_file_and_leaves_it_untouched(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.write_text("precious\n")
        message = manage.enable(asset, self.target, force=False)
        self.assertTrue(message.lstrip().startswith("!"))
        self.assertEqual(link.read_text(), "precious\n")

    def test_force_never_deletes_a_real_file(self):
        """The promise that matters: --force replaces symlinks, not files."""
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.write_text("precious\n")
        message = manage.enable(asset, self.target, force=True)
        self.assertTrue(message.lstrip().startswith("!"))
        self.assertTrue(link.is_file())
        self.assertEqual(link.read_text(), "precious\n")

    def test_refuses_a_foreign_symlink_without_force(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        elsewhere = self.repo / "agents" / ".hidden.md"
        link.symlink_to(elsewhere)
        message = manage.enable(asset, self.target, force=False)
        self.assertTrue(message.lstrip().startswith("!"))
        self.assertEqual(link.resolve(), elsewhere.resolve())

    def test_force_replaces_a_foreign_symlink(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.symlink_to(self.repo / "agents" / ".hidden.md")
        manage.enable(asset, self.target, force=True)
        self.assertEqual(link.resolve(), asset.source.resolve())


class TestDisable(RepoFixture):
    def test_removes_our_own_link(self):
        asset = self.asset("skills/demo")
        manage.enable(asset, self.target, force=False)
        manage.disable(asset, self.target)
        self.assertFalse(asset.link_path(self.target).exists())
        self.assertTrue(asset.source.exists(), "the asset itself must survive")

    def test_is_idempotent(self):
        asset = self.asset("skills/demo")
        self.assertIn("already disabled", manage.disable(asset, self.target))

    def test_leaves_a_real_file_alone(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        link.write_text("precious\n")
        message = manage.disable(asset, self.target)
        self.assertTrue(message.lstrip().startswith("!"))
        self.assertEqual(link.read_text(), "precious\n")

    def test_leaves_a_foreign_symlink_alone(self):
        asset = self.asset("agents/helper")
        link = asset.link_path(self.target)
        link.parent.mkdir(parents=True)
        elsewhere = self.repo / "agents" / ".hidden.md"
        link.symlink_to(elsewhere)
        message = manage.disable(asset, self.target)
        self.assertTrue(message.lstrip().startswith("!"))
        self.assertTrue(link.is_symlink())


class TestSelect(RepoFixture):
    def test_by_bare_name(self):
        chosen = manage.select(manage.discover(), ["demo"])
        self.assertEqual([a.qualified for a in chosen], ["skills/demo"])

    def test_by_qualified_name(self):
        chosen = manage.select(manage.discover(), ["agents/helper"])
        self.assertEqual([a.qualified for a in chosen], ["agents/helper"])

    def test_unknown_name_exits(self):
        with self.assertRaises(SystemExit) as caught:
            manage.select(manage.discover(), ["nope"])
        self.assertIn("no asset named", str(caught.exception))

    def test_ambiguous_name_exits_and_names_the_options(self):
        (self.repo / "hooks").mkdir()
        (self.repo / "hooks" / "demo").mkdir()
        with self.assertRaises(SystemExit) as caught:
            manage.select(manage.discover(), ["demo"])
        message = str(caught.exception)
        self.assertIn("ambiguous", message)
        self.assertIn("skills/demo", message)
        self.assertIn("hooks/demo", message)


if __name__ == "__main__":
    unittest.main()
