from click.testing import CliRunner
from kacl.kacl_cli import cli
from tests.snapshot_directory import snapshot_directory
from freezegun import freeze_time

import json
import os
import shutil

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

@freeze_time("2023-01-01")
def test_release_patch(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, 'CHANGELOG_with_changes.md')

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, 'CHANGELOG.md'))
        result = runner.invoke(
            cli,
            [
                '-f', 'CHANGELOG.md',
                "release",
                "patch",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)

@freeze_time("2023-01-01")
def test_release_minor(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, 'CHANGELOG_with_changes.md')

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, 'CHANGELOG.md'))
        result = runner.invoke(
            cli,
            [
                '-f', 'CHANGELOG.md',
                "release",
                "minor",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)

@freeze_time("2023-01-01")
def test_release_major(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, 'CHANGELOG_with_changes.md')

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, 'CHANGELOG.md'))
        result = runner.invoke(
            cli,
            [
                '-f', 'CHANGELOG.md',
                "release",
                "major",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)

@freeze_time("2023-01-01")
def test_release_custom(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, 'CHANGELOG_with_changes.md')

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, 'CHANGELOG.md'))
        result = runner.invoke(
            cli,
            [
                '-f', 'CHANGELOG.md',
                "release",
                "2.1.1",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)

@freeze_time("2023-01-01")
def test_add_change_security(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, 'CHANGELOG_with_changes.md')

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, 'CHANGELOG.md'))
        result = runner.invoke(
            cli,
            [
                '-f', 'CHANGELOG.md',
                "add",
                "Security",
                "Important Security Change",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_config(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")

    result = runner.invoke(
        cli,
        [
            '-c', os.path.join(resources_dir, 'config.yml'),
            '-f', 'CHANGELOG.md',
            'verify'
        ],
        catch_exceptions=False,
    )
    assert result.exit_code != 0, result.output

