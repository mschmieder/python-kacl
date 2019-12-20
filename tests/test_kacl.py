from unittest import TestCase

import kacl
import os

# from __future__ import print_function
import chalk


class TestKacl(TestCase):
    def test_load_valid(self):
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_1_1_0.md")
        changelog = kacl.load(changlog_file)

        self.assertEqual(changelog.title(), 'Changelog')
        self.assertGreater(len(changelog.versions()), 0)

        version = changelog.get('1.0.0')
        self.assertIsNotNone(version)

        added_changes = version.changes('Added')
        self.assertIsNotNone(added_changes)

        added_items = added_changes.items()
        self.assertIsNotNone(added_items)

    def test_dump(self):
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_1_1_0.md")
        changelog = kacl.load(changlog_file)
        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        with open(changlog_file, 'r') as reference_file:
            changelog_reference = reference_file.read()
        reference_file.close()

        changelog_dump_lines = changelog_dump.split('\n')
        changelog_reference_lines = changelog_reference.split('\n')

        self.assertEqual(len(changelog_dump_lines),
                         len(changelog_reference_lines))
        self.assertEqual(changelog_dump, changelog_reference)

    def test_add_change(self):
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_1_1_0.md")

        changelog = kacl.load(changlog_file)

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
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_1_1_0.md")
        changelog = kacl.load(changlog_file)

        msg = 'This is my first added change'
        changelog.add('Added', msg)
        changelog.release(version='2.0.0', link='https://my-new-version/2.0.0.html')

        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        changelog_changed = kacl.parse(changelog_dump)
        self.assertIsNotNone(changelog_changed)

        version = changelog_changed.get('2.0.0')
        self.assertIsNotNone(version)

        self.assertIn(msg, version.changes('Added').items())


    def test_invalid(self):
        filename='CHANGELOG_1_1_0_invalid.md'
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data", filename)
        changelog = kacl.load(changlog_file)
        self.assertFalse(changelog.is_valid())

    def test_valid(self):
        changlog_file = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data/CHANGELOG_1_1_0.md")
        changelog = kacl.load(changlog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_load_empty(self):
        changelog = kacl.parse("")
        self.assertFalse(changelog.is_valid())