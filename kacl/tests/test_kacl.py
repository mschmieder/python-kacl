from unittest import TestCase

import kacl
import os

class TestKacl(TestCase):
    def test_load_valid(self):
        changlog_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/CHANGELOG_1_1_0.md")
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
        changlog_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/CHANGELOG_1_1_0.md")
        changelog = kacl.load(changlog_file)
        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        with open(changlog_file, 'r') as reference_file:
            changelog_reference = reference_file.read()

        changelog_dump_lines = changelog_dump.split('\n')
        changelog_reference_lines = changelog_reference.split('\n')

        self.assertEqual(len(changelog_dump_lines), len(changelog_reference_lines))
        self.assertEqual(changelog_dump, changelog_reference)

        # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/CHANGELOG_1_1_0.dump.md"), 'w') as f:
        #     f.write(changelog_dump)
        # f.close()