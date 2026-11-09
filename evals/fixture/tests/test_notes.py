import unittest

from notes import make_title, word_count


class MakeTitleTest(unittest.TestCase):
    def test_NOTE_1_keeps_plain_title(self):
        self.assertEqual(make_title("Groceries"), "Groceries")


class WordCountTest(unittest.TestCase):
    def test_NOTE_3_counts_words(self):
        self.assertEqual(word_count("buy milk"), 2)
