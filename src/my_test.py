import re
from blocktype import block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from actions import markdown_to_blocks, split_nodes_image

#matches = re.findall(r"!\[(.*?)\]\((.*?)\)", "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
#print(matches)

#matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
#print(matches)

# node = TextNode(
#     "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
#     TextType.TEXT,
# )
# new_nodes = split_nodes_image([node])
# print(new_nodes)

