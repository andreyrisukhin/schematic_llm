"""
After getting json (rson) output from converter functions, remove quotes from the file.
This reduces tokens used.
"""

import os

def remove_quotes(file_path, new_file_path):
    # suffix = "_no_quotes"
    # new_file_path = file_path.replace(".json", f"{suffix}.json")
    with open(file_path, 'r') as f:
        data = f.read()
        data = data.replace('"', '')
    with open(new_file_path, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    dir = "../dataset/all_json"
    new_dir = "../dataset/all_json_no_quotes"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for file in os.listdir(dir):
        if file.endswith(".json"):
            file_path = os.path.join(dir, file)
            new_file_path = os.path.join(new_dir, file)
            remove_quotes(file_path, new_file_path)
            # print(f"Removed quotes from {file_path}")