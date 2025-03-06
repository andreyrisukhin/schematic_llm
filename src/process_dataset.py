"""
bulk process .schematic files to .json files
"""

import schem2rson
import os
import json

def main():
    dataset_dir = "../dataset/raw"
    output_dir = "../dataset/processed"

    skip_bedrock_files = [6726, 6722]

    # TODO skip command block files

    skip_files_with = ['minecraft:sign', 'age:']
    # Signs have too much info 22059.litematic
    # Different ages should be consolidated, for now skip farms

    # TODO skip "Properties" array in nbt data of a block, player can figure it out and takes up data
    # Assume piston always extended false, always facing north


    # TODO replace all respective non-redstone blocks to be transparent (glass), solid (stone)

    errored = []

    for file in os.listdir(dataset_dir):
        # if file.endswith(".schematic"):
        file_path = os.path.join(dataset_dir, file)
        try:
            data = schem2rson.schem_to_rson(file_path)
            output_file = os.path.join(output_dir, f'{file}.json')
            with open(output_file, 'w') as f:
                json.dump(data, f)

        except Exception as e:
            print(f'Error processing {file_path}: {e}')

            # Save error'd file strings, output to a file
            errored.append(file_path)

    with open('errored_files.txt', 'w') as f:
        for file in errored:
            f.write(f'{file}\n')


if __name__ == "__main__":
    main()