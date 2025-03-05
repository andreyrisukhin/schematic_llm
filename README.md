# schematic_llm

## Done
* RSON (RedStone Object Notation) of a 2x2 door is input to ChatGPT with a matching prompt, and ChatGPT returns well-formed RSON of a 2x3 door.
* Automatically evaluate RSON (block positions collide)

## TODO
* P0: Parse litematica --> RSON (create training data)
* P0: Parse RSON --> litematica (give user a schematic to test)
* P1: Load and evaluate the minecraft schematic (check door volume, toggle lever, check door volume) (return stone positions in debug information)
* P1: Add LLM api calls

## Maybe 
* If few shot prompt fails on complex tasks, finetune llm
* RSON piston placement validator? More work to calculate, firing seq important, maybe cheaper to just test in game simulator.



## Updates, Thoughts
* `litemapy` does not work with .schem files
* `minecraftschematics` also does not, due to version mismatch (schematic v2 accepted, we use schematic v3)
    * Converting?
    * Using an older version of minecraft?
    * Updating the minecraftschematics code?


Use `nbt -r ../schem/2x2door.schem > ../schem/2x2door_out` to convert via CLI

