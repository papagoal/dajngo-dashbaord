import os
from unittest import TestCase

from simpletail import ropen


class RopenTestCase(TestCase):
    def test_simple(self):
        filename = os.path.join("tests", "data", "simple.txt")
        with ropen(filename) as f:
            self.assertEqual(next(f), "Line 7\n")
            self.assertEqual(next(f), "Line 6\n")
            self.assertEqual(next(f), "Line 5\n")
            self.assertEqual(next(f), "Line 4\n")
            self.assertEqual(next(f), "Line 3\n")
            self.assertEqual(next(f), "Line 2\n")
            self.assertEqual(next(f), "Line 1\n")
            with self.assertRaises(StopIteration):
                next(f)

    def test_simple_readline(self):
        filename = os.path.join("tests", "data", "simple.txt")
        with ropen(filename) as f:
            self.assertEqual(f.readline(), "Line 7\n")
            self.assertEqual(f.readline(), "Line 6\n")
            self.assertEqual(f.readline(), "Line 5\n")
            self.assertEqual(f.readline(), "Line 4\n")
            self.assertEqual(f.readline(), "Line 3\n")
            self.assertEqual(f.readline(), "Line 2\n")
            self.assertEqual(f.readline(), "Line 1\n")
            self.assertEqual(f.readline(), "")
            self.assertEqual(f.readline(), "")
            self.assertEqual(f.readline(), "")

    def test_small_buffer(self):
        filename = os.path.join("tests", "data", "simple.txt")
        with ropen(filename, bufsize=3) as f:
            self.assertEqual(next(f), "Line 7\n")
            self.assertEqual(next(f), "Line 6\n")
            self.assertEqual(next(f), "Line 5\n")
            self.assertEqual(next(f), "Line 4\n")
            self.assertEqual(next(f), "Line 3\n")
            self.assertEqual(next(f), "Line 2\n")
            self.assertEqual(next(f), "Line 1\n")
            with self.assertRaises(StopIteration):
                next(f)

    def _check_utf(self, s, length, end):
        self.assertEqual(len(s), length)
        self.assertTrue(s.endswith(end))

    def test_utf_noeol(self):
        filename = os.path.join("tests", "data", "utf_noeol.txt")
        with ropen(filename, encoding="utf8") as f:
            self.assertEqual(next(f), "Γραμμή 7")
            self.assertEqual(next(f), "Γραμμή 6\n")
            self.assertEqual(next(f), "Γραμμή 5\n")
            self.assertEqual(next(f), "Γραμμή 4\n")
            self.assertEqual(next(f), "Γραμμή 3\n")
            self.assertEqual(next(f), "Γραμμή 2\n")
            self.assertEqual(next(f), "Γραμμή 1\n")
            with self.assertRaises(StopIteration):
                next(f)

    def test_utf_noeol_small_buffer(self):
        filename = os.path.join("tests", "data", "utf_noeol.txt")
        with ropen(filename, encoding="utf8", bufsize=3) as f:
            self.assertEqual(next(f), "Γραμμή 7")
            self.assertEqual(next(f), "Γραμμή 6\n")
            self.assertEqual(next(f), "Γραμμή 5\n")
            self.assertEqual(next(f), "Γραμμή 4\n")
            self.assertEqual(next(f), "Γραμμή 3\n")
            self.assertEqual(next(f), "Γραμμή 2\n")
            self.assertEqual(next(f), "Γραμμή 1\n")
            with self.assertRaises(StopIteration):
                next(f)
