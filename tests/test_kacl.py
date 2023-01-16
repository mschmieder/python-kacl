from unittest import TestCase

import kacl
from kacl.config import KACLConfig
import os
import yaml


class TestKacl(TestCase):
    def test_load_valid(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)

        self.assertEqual(changelog.title(), 'Changelog')
        self.assertGreater(len(changelog.versions()), 0)

        version = changelog.get('1.0.0')
        self.assertIsNotNone(version)

        added_changes = version.changes('Added')
        self.assertIsNotNone(added_changes)

        added_items = added_changes.items()
        self.assertIsNotNone(added_items)

    def test_dump(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)
        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        with open(changelog_file, 'r') as reference_file:
            changelog_reference = reference_file.read()
        reference_file.close()

        changelog_dump_lines = changelog_dump.split('\n')
        changelog_reference_lines = changelog_reference.split('\n')

        self.assertEqual(len(changelog_dump_lines),
                         len(changelog_reference_lines))
        self.assertEqual(changelog_dump, changelog_reference)

    def test_add_change(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")

        changelog = kacl.load(changelog_file)

        msg = 'This is my first added change'
        changelog.add('Added', msg)

        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        changelog_changed = kacl.parse(changelog_dump)
        self.assertIsNotNone(changelog_changed)

        unreleased = changelog_changed.get('Unreleased')
        self.assertIsNotNone(unreleased)

        unreleased_change_sections = unreleased.sections()
        self.assertIsNotNone(unreleased_change_sections)
        self.assertIn('Added', unreleased_change_sections)

        unreleased_changes_added = unreleased.changes('Added')
        self.assertIsNotNone(unreleased_changes_added)

        self.assertIn(msg, unreleased_changes_added.items())


    def test_release(self):
        valid_files = [
            'CHANGELOG.md',
            'CHANGELOG_unrelease_only.md'
        ]

        for filename in valid_files:
            changelog_file = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "data", filename)
            changelog = kacl.load(changelog_file)

            msg = 'This is my first added change'
            changelog.add('Added', msg)

            self.assertTrue(changelog.has_changes())

            changelog.release(version='2.0.0', link='https://my-new-version/2.0.0.html')

            changelog_dump = kacl.dump(changelog)
            self.assertIsNotNone(changelog_dump)

            changelog_changed = kacl.parse(changelog_dump)
            self.assertIsNotNone(changelog_changed)

            version = changelog_changed.get('2.0.0')
            self.assertIsNotNone(version)

            self.assertIn(msg, version.changes('Added').items())


    def test_invalid(self):
        invalid_files = [
            'CHANGELOG_invalid.md',
            'CHANGELOG_missing_sections.md',
            'CHANGELOG_no_unreleased.md'
        ]

        for filename in invalid_files:
            changelog_file = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "data", filename)
            changelog = kacl.load(changelog_file)
            self.assertFalse(changelog.is_valid())

    def test_valid(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_valid_keepachangelogcom(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_keepachangelog.com.md")
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_valid_project_changelog(self):
        changelog_file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), "CHANGELOG.md")
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_load_empty(self):
        changelog = kacl.parse("")
        self.assertFalse(changelog.is_valid())

    def test_release_without_changes(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_no_unreleased.md")
        changelog = kacl.load(changelog_file)

        self.assertFalse(changelog.has_changes())
        self.assertRaises(Exception, changelog.release, "1.1.1", 'https://github.com/mschmieder/python-kacl/compare/v1.0.0...HEAD' )


    def test_release_existing_version(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)

        msg = 'This is my first added change'
        changelog.add('Added', msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(Exception, changelog.release, "1.0.0", 'https://github.com/mschmieder/python-kacl/compare/v1.0.0...HEAD' )

    def test_release_without_older_version(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)

        msg = 'This is my first added change'
        changelog.add('Added', msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(Exception, changelog.release, "0.9.0", 'https://github.com/mschmieder/python-kacl/compare/v1.0.0...HEAD' )

    def test_release_with_non_semver(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")
        changelog = kacl.load(changelog_file)

        msg = 'This is my first added change'
        changelog.add('Added', msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(Exception, changelog.release, "a0.9.0", 'https://github.com/mschmieder/python-kacl/compare/v1.0.0...HEAD' )


    def test_release_with_increment(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.1.0",
            "patch": "1.0.1",
        }
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)

            msg = 'This is my first added change'
            changelog.add('Added', msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment = increment)
            self.assertEqual(expected_version, changelog.current_version())

        fail_tests = {
            "post": "1.0.0-post.1"
        }

        for increment, expected_version in fail_tests.items():
            changelog = kacl.load(changelog_file)

            msg = 'This is my first added change'
            changelog.add('Added', msg)

            self.assertTrue(changelog.has_changes())
            self.assertRaises(kacl.KACLException, changelog.release, increment=increment)

    def test_release_with_increment_extension(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.1.0",
            "patch": "1.0.1",
            "post": "1.0.0-post.1"
        }
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG.md")

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)
            changelog.config.post_release_version_prefix = 'post'

            msg = 'This is my first added change'
            changelog.add('Added', msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment = increment)
            self.assertEqual(expected_version, changelog.current_version())


    def test_post_release_with_increment(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.1.0",
            "patch": "1.0.1",
            "post": "1.0.0-post.2"
        }
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_post.md")

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)

            msg = 'This is my first added change'
            changelog.add('Added', msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment = increment)
            self.assertEqual(expected_version, changelog.current_version())


    def test_unreleased_missing_sections(self):
        changelog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_missing_sections.md")

        changelog = kacl.load(changelog_file)
        validation = changelog.validate()
        self.assertFalse(changelog.is_valid())

    def test_config(self):
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/config.yml")
        kacl_config = KACLConfig(config_file=config_file)

        default_config = dict()
        with open('kacl/config/kacl-default.yml', 'r') as f:
            default_config = yaml.safe_load(f)['kacl']

        # changes in config_file
        # changelog_file: CHANGELOG.md
        # allowed_header_titles:
        #   - ChangeLog
        # allowed_version_sections:
        #   - Security
        # git:
        #   commit: False

        self.assertNotEqual(kacl_config.allowed_header_titles, default_config['allowed_header_titles'] )
        self.assertEqual(kacl_config.allowed_header_titles, ['ChangeLog'] )

        self.assertNotEqual(kacl_config.allowed_version_sections, default_config['allowed_version_sections'] )
        self.assertEqual(kacl_config.allowed_version_sections, ['Security'] )

        self.assertNotEqual(kacl_config.git_create_commit, default_config['git']['commit'] )
        self.assertEqual(kacl_config.git_create_commit, True )


    def test_link_generation(self):
        valid_files = [
            #'CHANGELOG.md',
            'CHANGELOG_unrelease_only.md'
        ]

        for filename in valid_files:
            changelog_file = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "data", filename)
            changelog = kacl.load(changelog_file)

            changelog = kacl.load(changelog_file)
            changelog.generate_links()

            versions = changelog.versions()
            for v in versions:
                self.assertIsNotNone(v.link())
