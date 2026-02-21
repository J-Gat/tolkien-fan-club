import os

def delete_directory(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            delete_directory(item_path)
    os.rmdir(path)

def copy_directory(src, dst):
    if os.path.exists(dst):
        delete_directory(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying: {src_path} -> {dst_path}")
            with open(src_path, "rb") as f:
                content = f.read()
            with open(dst_path, "wb") as f:
                f.write(content)
        else:
            copy_directory(src_path, dst_path)

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            contents = file.read()
            file.close()
        return contents
    else:
        raise Exception(f"File not found: {path}")
    
def write_file(path, content):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(path, "w") as file:
        file.write(content)
        file.close()