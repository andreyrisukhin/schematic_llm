"""
Explore the schematic files, get out json data about each, in particular the blocks and their positions.
Format in a clear way to be used by the LLM to understand the schematic.
"""

import json
import os
import litemapy
import nbtlib

file = "../schematics/door 2x2.litematic"

def print_schematic_info(file):
    # Load the schematic file
    schematic = litemapy.Schematic.load(file)
    # print(f"{schematic.preview=}")

    nbt = schematic.to_nbt()
    # print(f"{type(nbt)=}\n{nbt=}")

    # Save NBT data to a file using nbtlib
    filepath, file_extension = os.path.splitext(file)
    nbt_file_path = f"{filepath}.nbt"
    # json_file_path = f"{filepath}.json"
    
    serialized = nbtlib.serialize_tag(nbt)  # Serialize the NBT data
    # Is there a way to save as json? Or another way to programmatically get out the coordinates data?
    explore = nbtlib.File(nbt)
    explore = explore["Regions"]
    print(f"{type(explore)=}")
    print(f"{explore.items()=}")
    for k, v in explore.items():
        print(f"{k=}, {v=}, \n")

    

    # (1) Access the BlockStates value to rewrite the long encodings of blocks into a format that is easier for LM to parse / manipulate (tokenization of numbers is unreliable).



    # print(f"{explore['Regions']['BlockStates']=}")

    # Save NBT to a binary file
    with open(nbt_file_path, "w") as f:
        # f.write(nbtlib.serialize(nbt))  # Serialize the NBT data to binary format
        # nbtlib.serialize(nbt, f)  # Serialize the NBT data directly to the file
        f.write(serialized)

    print(f"NBT data saved to {nbt_file_path}")

if __name__ == "__main__":
    print_schematic_info(file)







