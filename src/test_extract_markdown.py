import unittest

from actions import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_bad_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![asdf](https://i.imgur.com/zjjcJKZ.png) and anther ![hi](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("asdf", "https://i.imgur.com/zjjcJKZ.png"), ("hi", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_bad_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a ![link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [think](https://i.imgur.com/zjjcJKZ.png) and anther [dunk](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("think", "https://i.imgur.com/zjjcJKZ.png"), ("dunk", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_title(self):
        title = extract_title(
            "# This is the title\n\nThis is some text.\n\n## This is a subtitle"
        )
        self.assertEqual("This is the title", title)

    def test_extract_title_no_title(self):
        title = extract_title(
            "This is some text.\n\n## This is a subtitle"
        )
        self.assertEqual("Untitled", title)