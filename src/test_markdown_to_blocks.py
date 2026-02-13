import unittest
from actions import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_single_block(self):
            md = "This is a single paragraph with no extra whitespace"
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["This is a single paragraph with no extra whitespace"])

        def test_multiple_blank_lines(self):
            md = """Block 1


Block 2


Block 3"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

        def test_heading_blocks(self):
            md = """# Heading 1

Some text here

## Heading 2"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["# Heading 1", "Some text here", "## Heading 2"])

        def test_code_block(self):
            md = """```
code here
more code
```

Regular paragraph"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["```\ncode here\nmore code\n```", "Regular paragraph"])

        def test_empty_string(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])