from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)

            # If there is only one part, we're done
            if len(parts) == 1:
                new_nodes.append(node)
                continue

            # If the beginning or end of the node.text is the delimiter we need to remove those empty parts
            parts = [s for s in parts if s]

            # Normally the odd parts are the delimited text, but if node.text start with the delimiter then it's the even parts
            if node.text[0:len(delimiter)] == delimiter:
                even_is_TEXT = False
            else:
                even_is_TEXT = True

            # Now we check to ensure we had matching delimiters. Have to handle if the delimiter was at the end of node.text
            if len(parts) % 2 == 0:
                if even_is_TEXT and not node.text[-len(delimiter):] == delimiter:
                    raise Exception("Unmatched delimiter")
            else:
                if not even_is_TEXT:
                    raise Exception("Unmatched delimiter")

            # Now loop over the parts and create the new nodes
            i = 0            
            for part in parts:
                if (i if even_is_TEXT else i + 1) % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
                i += 1
    return new_nodes
