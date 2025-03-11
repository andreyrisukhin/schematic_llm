"""
Given a user parameter k, representing desired capacity, generate a schematic for a silo with k capacity.

Once coded, next steps include:
* Tiling Silos (space constraints)
"""

import mcschematic as ms

def add_base_layer(silo:ms.MCSchematic):
    # base_layer = ms.MCSchematic()
    silo.setBlock((0,0,0), "minecraft:stone")
    silo.setBlock((1,0,0), "minecraft:barrel")
    silo.setBlock((0,0,-1), "minecraft:quartz_block")
    silo.setBlock((1,0,-1), "minecraft:hopper[enabled=true,facing=south]")
    silo.setBlock((0,0,-2), "minecraft:hopper[enabled=true,facing=east]")
    silo.setBlock((1,0,-2), "minecraft:hopper[enabled=true,facing=south]")

    # base_layer.save(".", "silo_base", ms.Version.JE_1_18_2)
    return silo

def add_layer_A(silo:ms.MCSchematic, i:int):
    # layer_A = ms.MCSchematic()
    silo.setBlock((0,i,0), "minecraft:stone")
    silo.setBlock((1,i,0), "minecraft:redstone_lamp[lit=false]")
    silo.setBlock((0,i,-1), "minecraft:comparator[facing=north,mode=compare,powered=false]")

    silo.setBlock((0,i,-2), "minecraft:chest[facing=west,type=right,waterlogged=false]")
    silo.setBlock((1,i,-2), "minecraft:quartz_block")
    silo.setBlock((0,i,-3), "minecraft:chest[facing=west,type=left,waterlogged=false]")
    silo.setBlock((1,i,-3), "minecraft:hopper[enabled=true,facing=west]")
    
    # layer_A.save(".", "silo_layer_A", ms.Version.JE_1_18_2)
    return silo

def add_layer_B(silo:ms.MCSchematic, i:int):
    # layer_B = ms.MCSchematic()
    silo.setBlock((0,i,0), "minecraft:stone")
    silo.setBlock((1,i,0), "minecraft:redstone_lamp[lit=false]")
    silo.setBlock((0,i,-1), "minecraft:quartz_block")
    silo.setBlock((1,i,-1), "minecraft:quartz_block")
    silo.setBlock((0,i,-2), "minecraft:hopper[enabled=true,facing=north]")
    silo.setBlock((1,i,-2), "minecraft:comparator[facing=north,mode=compare,powered=false]")
    silo.setBlock((0,i,-3), "minecraft:chest[facing=north,type=left,waterlogged=false]")
    silo.setBlock((1,i,-3), "minecraft:chest[facing=north,type=right,waterlogged=false]")
    
    # layer_B.save(".", "silo_layer_B", ms.Version.JE_1_18_2)
    return silo

def generate_silo(k):
    """
    Parameters:
    k: int
        Desired capacity of the silo, inventory item slots.
    """
    assert k > 0, "Capacity must be greater than 0."

    capacity_base = 27 + (3*5)
    capacity_layer = (27*2) + 5

    layer_count = (k - capacity_base) // capacity_layer

    silo = ms.MCSchematic()
    silo = add_base_layer(silo)

    # Alternate A B layers until height is reached
    for l in range(layer_count):
        if l % 2 == 0:
            silo = add_layer_A(silo, l+1)
        else:
            silo = add_layer_B(silo, l+1)

    silo.save(".", f"silo_{k}", ms.Version.JE_1_18_2)


if __name__ == "__main__":
    generate_silo(1000)