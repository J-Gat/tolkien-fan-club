import unittest

from actions import extract_markdown_images, extract_markdown_links

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
