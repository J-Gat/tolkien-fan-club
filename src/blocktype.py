import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^- ", block):
        return BlockType.ULIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.OLIST
    elif re.match(r"^> ", block):
        return BlockType.QUOTE
    elif re.match(r"^```(.*)```", block, re.DOTALL):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
