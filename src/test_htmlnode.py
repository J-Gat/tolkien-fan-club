import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This links to Google", props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">This links to Google</a>')

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], props={"class": "my-span"})
        parent_node = ParentNode("div", [child_node], props={"class": "my-div"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="my-div"><span class="my-span"><b>grandchild</b></span></div>',
        )

    def test_to_html_with_multiple_grandchildren_with_props(self):
        grandchild_1_node = LeafNode("b", "grandchild 1")
        grandchild_2_node = LeafNode("i", "grandchild 2")
        child_node = ParentNode("span", [grandchild_1_node, grandchild_2_node], props={"class": "my-span"})
        parent_node = ParentNode("div", [child_node], props={"class": "my-div"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="my-div"><span class="my-span"><b>grandchild 1</b><i>grandchild 2</i></span></div>',
        )