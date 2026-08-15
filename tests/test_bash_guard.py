"""Tests for the Bash guard template — the parts its own cases cannot reach.

`bash_guard.py --selftest` proves *verdicts*: it calls `decide_bash` with a
command string and compares the answer. What it never exercises is the layer
Claude Code actually touches — a process, fed JSON on stdin, answering with
JSON on stdout — nor the helpers whose bugs are invisible end to end, because
a wrong `under()` or a wrong `strip_heredocs` shows up as a plausible verdict
rather than as an error.

That is the file whose failure mode is silence, so the plumbing is worth
pinning down separately from the rules.
"""

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

GUARD = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "specify"
    / "references"
    / "handoff-assets"
    / "bash_guard.py"
)

_SPEC = importlib.util.spec_from_file_location("bash_guard", GUARD)
guard = importlib.util.module_from_spec(_SPEC)
sys.modules["bash_guard"] = guard
_SPEC.loader.exec_module(guard)


def run_hook(payload, argv=()):
    """Feed the guard a payload the way the tool layer does."""
    return subprocess.run(
        [sys.executable, str(GUARD), *argv],
        input=payload if isinstance(payload, str) else json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )


def bash(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


class TestProcessContract(unittest.TestCase):
    """What the tool layer receives, rather than what `judge` returns."""

    def decision(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["hookSpecificOutput"]

    def test_a_silent_verdict_writes_nothing(self):
        result = run_hook(bash("git status"))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_a_deny_carries_the_event_name_and_a_reason(self):
        out = self.decision(run_hook(bash("git push --force origin main")))
        self.assertEqual(out["hookEventName"], "PreToolUse")
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertTrue(out["permissionDecisionReason"].strip())

    def test_an_ask_says_ask(self):
        out = self.decision(run_hook(bash("git push origin main")))
        self.assertEqual(out["permissionDecision"], "ask")

    def test_a_non_bash_tool_is_not_this_guard_s_business(self):
        payload = {"tool_name": "Read", "tool_input": {"file_path": "x"}}
        result = run_hook(payload)
        self.assertEqual(result.stdout.strip(), "")

    def test_a_missing_command_is_silence_not_a_crash(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {}})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_a_non_string_command_is_silence_not_a_crash(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": 7}})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_unparseable_input_asks_rather_than_failing_open(self):
        """A guard that cannot read its input must not wave the call
        through."""
        out = self.decision(run_hook("{not json"))
        self.assertEqual(out["permissionDecision"], "ask")
        self.assertIn("guard hook error", out["permissionDecisionReason"])

    def test_an_internal_error_asks(self):
        """The same promise for a failure anywhere below `decide`.

        A guard that crashes mid-decision must not let the call through: the
        hook layer would read silence as "no opinion". Forced here, because
        the failure this protects against is by definition one nobody
        anticipated.
        """
        def explode(*_args, **_kwargs):
            raise RuntimeError("boom")

        stdout = io.StringIO()
        stdin = io.StringIO(json.dumps(bash("git status")))
        with mock.patch.object(guard, "decide", explode), \
                mock.patch.object(guard.sys, "stdin", stdin), \
                contextlib.redirect_stdout(stdout):
            code = guard.main()
        out = json.loads(stdout.getvalue())["hookSpecificOutput"]
        self.assertEqual(code, 0)
        self.assertEqual(out["permissionDecision"], "ask")
        self.assertIn("boom", out["permissionDecisionReason"])


class TestSelftestEntryPoints(unittest.TestCase):
    def test_selftest_passes_and_reports_coverage(self):
        result = run_hook("", argv=("--selftest",))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("rules and grants covered", result.stdout)

    def test_liveness_passes_and_is_one_line(self):
        result = run_hook("", argv=("--liveness",))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("liveness:", result.stdout)
        self.assertNotIn("DEAD", result.stdout)


class TestHeredocs(unittest.TestCase):
    """A body is data, unless the thing being fed is a shell."""

    def test_a_shell_body_is_kept_because_it_runs(self):
        command = "bash <<'SH'\ngit push --force\nSH"
        self.assertIn("git push --force", guard.strip_heredocs(command))

    def test_another_language_s_body_is_data(self):
        command = "python3 - <<'PY'\ns = 'git push --force'\nPY"
        self.assertNotIn("git push --force", guard.strip_heredocs(command))

    def test_an_ordinary_body_is_data(self):
        command = "cat <<'EOF'\ngit push --force\nEOF"
        self.assertNotIn("git push --force", guard.strip_heredocs(command))


class TestEmbeddedCommands(unittest.TestCase):
    """A substitution that survives tokenizing, read off the raw line."""

    def test_double_quoted_substitution_is_found(self):
        self.assertEqual(
            guard.embedded_commands('git commit -m "$(cat msg)"'), ["cat msg"]
        )

    def test_backticks_are_found(self):
        self.assertEqual(guard.embedded_commands("echo `id -u`"), ["id -u"])

    def test_single_quotes_run_nothing_so_nothing_is_found(self):
        self.assertEqual(guard.embedded_commands("echo '$(id -u)'"), [])

    def test_nesting_is_counted_not_guessed(self):
        found = guard.embedded_commands('x "$(a $(b))"')
        self.assertEqual(found, ["a $(b)"])

    def test_an_unbalanced_substitution_stops_rather_than_guessing(self):
        self.assertEqual(guard.embedded_commands('x "$(a'), [])


class TestUnder(unittest.TestCase):
    """Paths are resolved before comparison, which is the whole point."""

    def test_a_path_inside_matches(self):
        self.assertTrue(guard.under("/tmp")("/tmp/build/x"))

    def test_the_location_itself_matches(self):
        self.assertTrue(guard.under("/tmp")("/tmp"))

    def test_traversal_out_does_not_match(self):
        self.assertFalse(guard.under("/tmp")("/tmp/../etc/passwd"))

    def test_a_prefix_that_is_not_a_parent_does_not_match(self):
        self.assertFalse(guard.under("/tmp")("/tmpfoo/x"))

    def test_a_glob_does_not_cross_a_separator(self):
        matcher = guard.under("/home/*/scratch")
        self.assertTrue(matcher("/home/yann/scratch/x"))
        self.assertFalse(matcher("/home/a/b/scratch/x"))

    def test_a_relative_path_matches_no_absolute_location(self):
        self.assertFalse(guard.under("/tmp")("build/x"))


class TestOperandQuantifier(unittest.TestCase):
    """`any_of` is the quantifier; a matcher alone cannot express it."""

    def test_every_operand_must_match_by_default(self):
        matcher = guard.under(".local")
        inside = [".local/a", ".local/b"]
        self.assertTrue(guard.operands_match(matcher, inside))
        self.assertFalse(guard.operands_match(matcher, [".local/a", "src"]))

    def test_any_of_needs_only_one(self):
        matcher = guard.any_of(guard.re.compile(r"^list$"))
        self.assertTrue(guard.operands_match(matcher, ["server", "list"]))
        self.assertFalse(guard.operands_match(matcher, ["server", "delete"]))

    def test_no_operands_never_matches(self):
        self.assertFalse(guard.operands_match(guard.under("/tmp"), []))


class TestCitation(unittest.TestCase):
    """A verdict has to say what it read, or a false positive is unfindable."""

    def reason(self, command):
        result = run_hook(bash(command))
        out = json.loads(result.stdout)["hookSpecificOutput"]
        return out["permissionDecisionReason"]

    def test_a_rule_names_itself_and_the_token_that_matched(self):
        reason = self.reason("git commit -a --amend -m x")
        self.assertIn("[rule git commit: --amend]", reason)

    def test_a_gated_verdict_names_the_invocation_instead(self):
        """Through the engine fixture: the shipped registry declares no
        grants, so a gated verdict is not reachable from its own tools."""
        # An unknown verb: no rule matches it, so the gated verdict is what
        # answers — which is the branch with no rule to cite.
        verdict = guard.decide_bash(
            "stubcli server frobnicate x", guard.registry(guard.STUBCLI)
        )
        self.assertIsNotNone(verdict)
        self.assertIn("no proven-safe shape", verdict[1])
        self.assertIn("stubcli server frobnicate", verdict[1])


if __name__ == "__main__":
    unittest.main()
