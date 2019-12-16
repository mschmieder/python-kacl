from unittest import TestCase

import kacl
import os

class TestKacl(TestCase):
    def test_load(self):
        kacl_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/CHANGELOG_1_1_0.md")
        doc = kacl.load(kacl_file)