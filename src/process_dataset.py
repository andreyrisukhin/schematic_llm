"""
bulk process .schematic files to .json files
"""

from schem2rson import schem_to_rson, litematic_to_rson, schematic_to_rson

import os
import json

def main():
    dataset_dir = "../dataset/raw"
    output_dir = "../dataset/all_json"

    vol_limit = 1700

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
        if file.endswith(".schematic"):
            
            # continue # Until I parse the blocks well
            
            file_path = os.path.join(dataset_dir, file)
            try:
                data = schematic_to_rson(file_path)
                # # If data is too big, skip
                # if data['volume_width'] * data['volume_height'] * data['volume_length'] > vol_limit:
                #     continue

                output_file = os.path.join(output_dir, f'{file}.json')
                with open(output_file, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print(f'Error processing {file_path}: {e}')
                errored.append(file_path)

        elif file.endswith(".litematic"):
            file_path = os.path.join(dataset_dir, file)
            try:
                data = litematic_to_rson(file_path)
                # # If data is too big, skip
                # if data['volume_width'] * data['volume_height'] * data['volume_length'] > vol_limit:
                #     continue

                # If data blocks has weird longs, skip
                # if any([any([any([len(str(b)) > 4 for b in row]) for row in layer]) for layer in data['block_positions']]):
                #     continue

                if data:
                    output_file = os.path.join(output_dir, f'{file}.json')
                    with open(output_file, 'w') as f:
                        json.dump(data, f)
            except Exception as e:
                print(f'Error processing {file_path}: {e}')
                errored.append(file_path)

        elif file.endswith(".schem"):                
            file_path = os.path.join(dataset_dir, file)
            try:
                data = schem_to_rson(file_path)

                # # If data is too big, skip
                # if data['volume_width'] * data['volume_height'] * data['volume_length'] > vol_limit:
                #     continue

                output_file = os.path.join(output_dir, f'{file}.json')
                with open(output_file, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print(f'Error processing {file_path}: {e}')
                errored.append(file_path)

    with open('errored_files.txt', 'w') as f:
        for file in errored:
            f.write(f'{file}\n')


if __name__ == "__main__":
    main()