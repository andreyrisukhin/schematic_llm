"""
Read the /raw/minecraft_schematic_data.json file, keep the idxs with a description that contains "door" as a list.
Then, given a dir, copy only the files with the idxs in the list to a second new dir.
"""

import json
import os
import shutil


def main():
    # Read the json file
    with open("../dataset/raw/minecraft_schematic_data.json") as f:
        data = json.load(f)

    # Get the idxs with a description that contains "door"
    door_idxs = [idx for idx, info in data.items() if "door" in info["description"]]
    print(door_idxs)        

    # Copy the files with the idxs in the list to a new dir
    src_dir = "../dataset/no_air_no_quotes_no_minecraft"
    dst_dir = "../dataset/doors_clean"
    os.makedirs(dst_dir, exist_ok=True)
    
    for file in os.listdir(src_dir):
        idx = file.split(".")[0]
        if idx in door_idxs:
            shutil.copyfile(os.path.join(src_dir, file), os.path.join(dst_dir, file))


if __name__ == "__main__":
    main()

