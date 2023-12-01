"""aoc2023 CLI tests."""

from click.testing import CliRunner

from aoc2023.__main__ import cli


def test_cli() -> None:
    """Test the Click CLI execution."""
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0


def test_cli_help() -> None:
    """Test CLI help generation."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "--help" in result.output
    assert "Show this message and exit." in result.output
