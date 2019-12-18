from unittest import TestCase

import kacl
import os

class TestKacl(TestCase):
    def test_load(self):
        kacl_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/CHANGELOG_1_1_0.md")
        doc = kacl.load(kacl_file)

        self.assertEqual(doc.title(), 'Changelog')
        self.assertGreater(len(doc.versions()), 0)

        version = doc.get('1.0.0')
        self.assertIsNotNone(version)

        added_changes = version.changes('Added')
        self.assertIsNotNone(added_changes)

        added_items = added_changes.items()
        self.assertIsNotNone(added_items)
