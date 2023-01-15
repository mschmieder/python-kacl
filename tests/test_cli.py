from click.testing import CliRunner
from kacl.kacl_cli import cli

import json

def test_verify():
    runner = CliRunner()
    result = runner.invoke(cli, ['-f', 'tests/data/CHANGELOG.md' , 'verify'])
    assert result.exit_code == 0
    assert result.output == 'Success\n'

    result = runner.invoke(cli, ['-f', 'tests/data/CHANGELOG_invalid.md' , 'verify'])
    assert result.exit_code == 10 # spawns 8 errors

def test_verify_with_json_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['-f', 'tests/data/CHANGELOG_invalid.md', 'verify', '--json'])
    validation_result = json.loads(result.output)

    assert len(validation_result["errors"]) == 10
    assert validation_result["valid"] == False