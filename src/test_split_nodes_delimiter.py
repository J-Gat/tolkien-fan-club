import unittest
from textnode import TextNode, TextType
from actions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        for n in new_nodes:
            self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_code_at_end(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        for n in new_nodes:
            self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE)])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        for n in new_nodes:
            self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_italic_at_start(self):
        node = TextNode("_This_ is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        for n in new_nodes:
            self.assertEqual(new_nodes, [TextNode("This", TextType.ITALIC), TextNode(" is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_italic_at_start_unmatched_delimiters(self):
        node = TextNode("_This_ is text with an italic_ word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_split_nodes_delimiter_bold__missing_at_start_unmatched_delimiters(self):
        node = TextNode("This** is text with a **bold** word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_mixed_delimiters(self):
        node = TextNode("_This_ is **text** with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        for n in new_nodes:
            self.assertEqual(new_nodes, [TextNode("This", TextType.ITALIC), TextNode(" is **text** with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()
