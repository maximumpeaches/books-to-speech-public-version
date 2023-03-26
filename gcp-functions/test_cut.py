import unittest

from book import cut_text


class TestCut(unittest.TestCase):
    def test_cut_text_inclusive(self):
        """
        Test that text is cut, including the end.
        """
        start = 'a cat'
        end = 'like'
        text = 'I am a cat I like a lot.'
        self.assertEqual('a cat I like', cut_text(text, start, end, True))

    def test_cut_text_exclusive(self):
        """
        Test that text is cut, excluding the end.
        """
        start = 'a cat'
        end = 'like'
        text = 'I am a cat I like a lot.'
        self.assertEqual('a cat I', cut_text(text, start, end, False))


if __name__ == '__main__':
    unittest.main()
