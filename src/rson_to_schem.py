"""
Given RSON output from LM, convert to a schematic.
"""

import json

def rson_to_schem(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # print(f'{data=}')
    for e in data:
        print(f'{e=}')


if __name__ == '__main__':

    file = "../rson_output/output_from_lm.json"
    rson_to_schem(file)

