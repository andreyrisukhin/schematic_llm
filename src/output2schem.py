"""
Read in a text file (output from the llm), and parse it into a dict of block and coordinate triples.
Then assemble the blocks into a schematic.
"""

from typing import Dict, List, Tuple

def file_to_text(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return text

def verify_syntax(text) -> str:
    """
    Count matching parentheses and brackets and braces.
    If the counts are equal or can be fixed by removing the last one, return text that works.
    Else raise an error.
    """

    stack = []
    for i, char in enumerate(text):
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack:
                # If the last character is unmatched, remove it and return the text
                if i == len(text) - 1:
                    return text[:-1]
                else:
                    raise ValueError(f"Unmatched closing {char} at position {i}")
            top = stack.pop()
            if (top == '(' and char != ')') or \
               (top == '[' and char != ']') or \
               (top == '{' and char != '}'):
                raise ValueError(f"Mismatched {top} and {char} at position {i}")
    if stack:
        raise ValueError(f"Unmatched opening {stack[-1]} at position {len(text)}")
    return text


def text_to_blocks(text) -> Dict[str, List[Tuple[int, int, int]]]:
    """
    Given text with matched {[()]}, with form {key: [[x1, y1, z1], [x2, y2, z2], ...]},
    return a dict of block names and coordinates.
    """
    blocks = {}

    text = text[1:-1] # Remove the outer { }

    parts = text.split("]],") # Split by "]],"
    for part in parts:
        part += "]]" # Add the missing ]]
        part = part.replace(' ', '')
        key, value = part.split(":")
        value = value[1:-1] # Remove the outer [ ]
        tuples = value.split("],") # Split values into the [x,y,z] tuples
        tuples = [t.replace('[', '').replace(']', '') for t in tuples]

        coords = []
        for t in tuples:
            x, y, z = t.split(',')
            coords.append((int(x), int(y), int(z)))
            
        blocks[key] = coords
    return blocks

def blocks_to_schem(blocks):
    """Given a dict of str blocks and their coordinates, return a schematic."""

    

if __name__ == '__main__':
    # import sys
    # if len(sys.argv) != 2:
    #     print("Usage: python output2schem.py <filename>")
    #     sys.exit(1)
    # filename = sys.argv[1]

    # Bad Syntax
    # filename = '../llm_output/Title_ 3x3 piston door Width_ 7 Height_ 9 Length_ 3'
    
    # Good Syntax
    filename = '../llm_output/Title_ Compact Angle Cannon Width_ 6 Height_ 4 Length_ 6'
    # filename = '../llm_output/Title_ FarmFish Width_ 5 Height_ 4 Length_ 7'

    text = file_to_text(filename)
    text = verify_syntax(text)
    blocks = text_to_blocks(text)
    print(blocks)