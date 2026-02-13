import unittest
from textnode import TextNode, TextType
from actions import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_multiple_bold_and_italic(self):
        text = "**bold1** and **bold2** _italic1_ and _italic2_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic1", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic2", TextType.ITALIC),
            ],
            nodes,
        )

    def test_code_and_link(self):
        text = "Here is `code` and a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_image_at_start_and_end(self):
        text = "![start](url1) middle text ![end](url2)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "url1"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "url2"),
            ],
            nodes,
        )

    def test_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
            ],
            nodes)

    