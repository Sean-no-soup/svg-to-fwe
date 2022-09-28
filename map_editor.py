#Ximsa's map editor
import matplotlib.pyplot as plt
import math
import struct
import sys

class Flags:
    WindFloor = 1 << (8*0)
    ViewFloor = 1 << (8*1)
    NoDraw = 1 << (8*2)
    Foundations = 1 << (8*3)
    Mines = 1 << (8*4)
    OilDrills = 1 << (8*5)
    OilRigs = 1 << (8*6) + 0
    PassProjectiles = 1 << (8*6) + 1
    PassBeams = 1 << (8*6) + 2
    Hazard = 1 << (8*6) + 3
    NoSplash = 1 << (8*6) + 4
    NoBuild = 1 << (8*6) + 5
    def remove(blockFlags, flag):
        return (blockFlags & ~flag)
    def set(blockFlags, flag):
        return (blockFlags | flag)
    def isFlagSet(blockFlags, flag):
        return (blockFlags & flag) != 0
    def readable(blockFlags):
        return list(filter(lambda xs: type(getattr(Flags, xs)) == type(1) and Flags.isFlagSet(blockFlags, getattr(Flags, xs)), dir(Flags))) # functional ftw


class Header:
    def __init__(self
                 ,head = bytearray.fromhex("1400 0000 0000 0000 0040 7544 0000 0000")
                 ,bounds = [-11000,11000,-11000,11000] # LRTB
                 ,environment = "environment/alpine"):
        self.head = head                                                 
        self.bounds = bounds
        self.environment = environment


class Node:
    def __init__(self
               ,point = [0,0,0] # x, y, z
               ,surface_name = ""):
        self.point = point
        self.surface_name = surface_name

class Block:
    def __init__(self
                 ,block_name = ""
                 ,colour = [1,1,1,1]
                 ,global_surface_name = ""
                 ,teamid = 0
                 ,flags = Flags.Foundations | Flags.Mines
                 ,terrain_name = "environment/alpine/ground/ground1.dds"
                 ,nodes = []):
        self.block_name = block_name
        self.colour = colour
        self.global_surface_name = global_surface_name
        self.teamid = teamid
        self.flags = flags
        self.terrain_name = terrain_name
        self.nodes = nodes
    def node_list(self):
         return list(map(
             lambda node: node.point,
                self.nodes))
        
        
class MapEditor:
    # creates a new instance, if filename exists will parse the contents of that file, else creates a empty project
    def __init__(self, filename):
        self.filename = filename
        self.blocks = []
        try:
            with open(filename, "rb") as f:
                self.parse(bytearray(f.read()))
                f.close()
        except FileNotFoundError:
            self.header = Header()
            self.footer = bytearray.fromhex("0000 0000 0000 0000 0000 0000")

    def save(self, filename = ""):
        if filename == "": filename = self.filename
        with open(filename, "wb") as f:
            contents = bytearray()
            # header
            contents += self.header.head
            # bounds
            contents += struct.pack('<ffff', *self.header.bounds)
            # env string length
            contents += struct.pack('<i', len(self.header.environment))
            # env string
            contents += self.header.environment.encode('utf-8')
            # blockcount
            contents += struct.pack('<i', len(self.blocks))
            for block in self.blocks:
                # block name length
                contents += struct.pack('<i', len(block.block_name))
                # block name
                contents += block.block_name.encode('utf-8')
                # node count
                contents += struct.pack('<i', len(block.nodes))
                # colour
                contents += struct.pack('<ffff', *block.colour)
                # terrain name length
                contents += struct.pack('<i', len(block.terrain_name))
                # terrain name
                contents += block.terrain_name.encode('utf-8')
                # global surface name length
                contents += struct.pack('<i', len(block.global_surface_name))
                # global surface name
                contents += block.global_surface_name.encode('utf-8')
                # const(?)
                contents += bytearray.fromhex("0000 c03e 0000 0000 0000 0000 0000 0000 0000 0000")
                # teamid
                contents += struct.pack('<i', block.teamid)
                #flags
                contents += struct.pack('<Q', block.flags)[:-1]
                # points
                for node in block.nodes:
                    # x,y,z
                    contents += struct.pack('<fff',*node.point)
                    # const (?)
                    contents += bytearray.fromhex("0000 0000")
                    # surface name length
                    contents += struct.pack('<i', len(node.surface_name))
                    # surface name
                    contents += node.surface_name.encode('utf-8')
            contents += self.footer
            f.write(contents)
            f.close()
            
    # parses bytearray
    def parse(self, contents):
        # header
        head = contents[:16]
        contents = contents[16:]
        # read in bounds
        bounds = struct.unpack('<ffff',contents[:16])
        contents = contents[16:]
        # read in env string length
        environment_length = struct.unpack('<i', contents[:4])[0]
        contents = contents[4:]
        # read in env string
        environment = contents[:environment_length].decode('utf-8')
        contents = contents[environment_length:]
        # save header
        self.header = Header(head, bounds, environment)
        # read in blockcount
        block_count = struct.unpack('<i', contents[:4])[0]
        contents = contents[4:]
        
        for block_number in range(block_count):
            # read in block name length
            block_name_length = struct.unpack('<i', contents[:4])[0]
            contents = contents[4:]
            # read in block name
            block_name = contents[:block_name_length].decode('utf-8')
            contents = contents[block_name_length:]
            # read in node count
            node_count = struct.unpack('<i', contents[:4])[0]
            contents = contents[4:]
            # read in colour
            colour = struct.unpack('<ffff',contents[:16])
            contents = contents[16:]
            # read in terrain name length
            terrain_name_length = struct.unpack('<i', contents[:4])[0]
            contents = contents[4:]
            # read in terrain name
            terrain_name = contents[:terrain_name_length].decode('utf-8')
            contents = contents[terrain_name_length:]
            # read in global surface name length
            global_surface_name_length = struct.unpack('<i', contents[:4])[0]
            contents = contents[4:]
            # read in global surface name name
            global_surface_name = contents[:global_surface_name_length].decode('utf-8')
            contents = contents[global_surface_name_length:]
            # skip const(?) 20 bytes
            contents = contents[20:]
            # read in teamid
            teamid = struct.unpack('<i', contents[:4])[0]
            contents = contents[4:]
            # read in flags
            flags = contents[:7]
            flags.append(0)
            flags = struct.unpack('<Q', flags)[0]
            contents = contents[7:]
            # read in nodes
            nodes = []
            for nodeIndex in range(node_count):
                # read in point
                point = struct.unpack('<fff',contents[:12])
                contents = contents[12:]
                # skip const(?) 4 bytes
                contents = contents[4:]
                # read in global surface name length
                surface_name_length = struct.unpack('<i', contents[:4])[0]
                contents = contents[4:]
                # read in global surface name name
                surface_name = contents[:surface_name_length].decode('utf-8')
                contents = contents[surface_name_length:]
                nodes.append(Node(point,surface_name))
            self.blocks.append(Block(block_name
                                     ,colour
                                     ,global_surface_name
                                     ,teamid
                                     ,flags
                                     ,terrain_name
                                     ,nodes))
        self.footer = contents
    def polygon_list(self):
        return list(map(
            lambda block: block.node_list(),
            self.blocks))
    
    def plot(self):
        polygons = list(map(lambda polygon: polygon + [polygon[0]], self.polygon_list()))
        plt.figure()
        for index, polygon in enumerate(polygons):
            xs, ys, _ = zip(*polygon)
            plt.plot(xs,list(map(lambda y: -y,ys)), c=plt.cm.jet(((self.blocks[index].flags * 31337 + 42069 )% 13)/13.0)) # color somewhat reflects blockflags
        plt.axis('scaled')
        plt.show()
        

#editor = MapEditor("playermap1.fwe")
#for block in editor.blocks:
#    if block.teamid == 1 or block.teamid == 2:
#        print(block.nodes[1].point)
#editor.header.bounds = [-11000, 11000, -11000, 11000]
#editor.save()
#editor = MapEditor("../Dueling Vipers 4v4/Dueling Vipers 4v4.fwe")
#print(editor.header.bounds)

#editor.blocks[0].colour = [100000,-10,-10,1]
#editor.blocks[1].colour = [1,-1,-1,1]
#editor.blocks[2].colour = [1,0,0,1]
#editor.blocks[3].colour = [10000,1,1,1]
#editor.plot()

