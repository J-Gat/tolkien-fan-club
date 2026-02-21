import os
import sys

from textnode import TextNode, TextType
from file_operations import copy_directory, read_file, write_file
from actions import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    template = read_file(template_path)
    
    for item in os.listdir(from_path):
        src_path = os.path.join(from_path, item)
        dst_path = os.path.join(dest_path, item)

        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            generate_page(src_path, template_path, dst_path, basepath)

        elif item.endswith(".md"):
            target_filename = item[:-3] + ".html"
            dst_path = os.path.join(dest_path, target_filename)
            print(f"Processing: {src_path} -> {dst_path}")

            markdown = read_file(src_path)

            html_nodes = markdown_to_html_node(markdown)
            html = html_nodes.to_html()

            title = extract_title(markdown)

            page = template.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", html)

            page = page.replace('href="/', f'href="{basepath}')
            page = page.replace('src="/', f'src="{basepath}')

            write_file(dst_path, page)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_directory("static", "docs")
    generate_page("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
    main()
