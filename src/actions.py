import re
from textnode import TextNode, TextType, text_node_to_html_node
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # Count delimiters early to check for balance
            delimiter_count = node.text.count(delimiter)
            if delimiter_count % 2 == 1:
                # Odd number of delimiters means they're unmatched
                raise Exception(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
            if delimiter_count == 0:
                # No delimiters, just append and continue
                new_nodes.append(node)
                continue
            
            parts = node.text.split(delimiter)

            # If the beginning or end of the node.text is the delimiter we need to remove those empty parts
            parts = [s for s in parts if s]

            # Normally the odd parts are the delimited text, but if node.text start with the delimiter then it's the even parts
            if node.text[0:len(delimiter)] == delimiter:
                even_is_TEXT = False
            else:
                even_is_TEXT = True

            # Now loop over the parts and create the new nodes
            i = 0            
            for part in parts:
                if (i if even_is_TEXT else i + 1) % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
                i += 1
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images:
            for image in images:
                sections = node.text.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) == 1:
                    new_nodes.append(node)
                else:
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        node.text = node.text[len(sections[0]):]
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    node.text = node.text[len(f"![{image[0]}]({image[1]})"):]
            if node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links:
            for link in links:
                sections = node.text.split(f"[{link[0]}]({link[1]})", 1)
                if len(sections) == 1:
                    new_nodes.append(node)
                else:
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        node.text = node.text[len(sections[0]):]
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    node.text = node.text[len(f"[{link[0]}]({link[1]})"):]
            if node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    return "Untitled"
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    parents = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            count = len(block) - len(block.lstrip('#'))
            children = block.lstrip('#').strip()
            parents.append(ParentNode(f"h{count}", text_to_children(children)))
           
        elif block_type == BlockType.ULIST:
            children = multiline_markdown_text_to_children(block, "- ", "li")
            parents.append(ParentNode("ul", children))

        elif block_type == BlockType.OLIST:
            children = multiline_markdown_OLIST_text_to_children(block)
            parents.append(ParentNode("ol", children))

        elif block_type == BlockType.QUOTE:
            child = ""
            for line in block.split("\n"):
                child += line.lstrip("> ") + " "
            children = text_to_children(child)
            parents.append(ParentNode("blockquote", children))

        elif block_type == BlockType.CODE:
            block = block.strip("`").lstrip("\n")
            parents.append(ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))]))

        else:
            parents.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
    
    return ParentNode("div", parents)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def multiline_markdown_text_to_children(text, prefix, html_tag):
    lines = text.split("\n")
    children = []
    for line in lines:
        line = line.lstrip(prefix)
        children.append(ParentNode(html_tag, text_to_children(line)))
    return children

def multiline_markdown_OLIST_text_to_children(text):
    lines = text.split("\n")
    children = []
    for line in lines:
        line = line.split(". ", 1)[1]
        children.append(ParentNode("li", text_to_children(line)))
    return children