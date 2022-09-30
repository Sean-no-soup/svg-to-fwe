#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:
  #print('loading dependencies\n\tmap_editor')
  import map_editor as ximsa
  #print('\tos')
  import os
  #print('\tnumpy')
  import numpy as np
  #print('\titertools')
  import itertools
  #print('\txml.dom')
  from xml.dom import minidom
  #print('\tsvg.path')
  from svg.path import parse_path
  from svg.path.path import Move
  from svg.path.path import Line
  from svg.path.path import Close
  from svg.path.path import CubicBezier
except:
  print('t\missing dependency')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions
def get_cubic_bezier_point(t, p):
    #t: curve parameter 0 to 1
    #p: list of 4 cubic bezier points each in a list [[x0,y0],[a,b],[c,d],[x1,y1]] ?
  multipliers = [
    t * t * t,
    3 * t * t * (1 - t),
    3 * t * (1 - t) * (1 - t),
    (1 - t) * (1 - t) * (1 - t)
  ]
  x = 0
  y = 0
  for index in range(4):
    x += p[index][0] * multipliers[index]
    y += p[index][1] * multipliers[index]
  return [x,y]

def get_arc_points(t,p):
  pass

def yn(text):
    if text.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:return True
    return False
    
def getPathStyleAttribute(path_style,attribute):
  attributeList = str(path_style).split(';')
  for item in attributeList:
    if item.split(':')[0]==attribute:return item.split(':')[1]
  return

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#find files
listVectorFile = []
listMapFile = []
for file in os.listdir():
    if file.endswith(".svg") : listVectorFile.append(file)
    if file.endswith(".fwe") : listMapFile.append(file)
    
assert len(listVectorFile) > 0, "'.svg' Vector file not found"
print('\nwhich vector file?')
for n in range(len(listVectorFile)):
    print('   {}:{}'.format(n,listVectorFile[n]))
vectorFile = listVectorFile[int(input())]
print('-----------------------------')


print('which terrain file?\n   0:make a new file')
for n in range(len(listMapFile)):
    print('   {}:{}'.format(n+1,listMapFile[n]))
terrain_choice = int(input())
if terrain_choice == 0: mapFile = str(input('new map name:'))+'.fwe'
else: mapFile = listMapFile[terrain_choice-1]
#print('-----------------------------')#########################################################################################################

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get/set some map/block variables for constructing the fwe
blockflags = 0
blocksurface = ''
blockterrain = "ui/textures/FE-Panel.tga"

#blockname = '' if yn(input('flag terrain to not be destructible (when used with destructable terrain mod) (y/n)?\n')) else 'a' ###############################
blockname = 'block'
#print('-----------------------------')#########################################################################################################
blockteamid = 3#int(input('terrain team?\n   1:team 1\n   2:team 2\n   3:any team\n   4:no team\n   5:background\n'))##########################for the sake of testing quickly
#print('-----------------------------')####################################################################################################
#print('terrain flags')#########################################################################################################################
flags = [
     ximsa.Flags.WindFloor,
     ximsa.Flags.ViewFloor,
     ximsa.Flags.NoDraw,
     ximsa.Flags.Foundations,
     ximsa.Flags.Mines,
     ximsa.Flags.OilDrills,
     ximsa.Flags.OilRigs,
     ximsa.Flags.PassProjectiles,
     ximsa.Flags.PassBeams,
     ximsa.Flags.Hazard,
     ximsa.Flags.NoSplash,
     ximsa.Flags.NoBuild]
for n in range(12):
    #print('{} (y/n)?'.format(str(ximsa.Flags.readable(flags[n]))))
    #flagbool = yn(input())  for the sake of testing things ########################################################################################
    flagbool = False
    if flagbool: blockflags = ximsa.Flags.set(blockflags, flags[n])
print('-----------------------------')

    
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#confirm
print("add the vectors in {} to the file '{}' \nteam {} with flags{}, \nand blocks named '{}'\n(y/n)?\n".format(vectorFile,mapFile,blockteamid,ximsa.Flags.readable(blockflags),blockname),end = '')
if not yn(input()):
  print('exit')
  quit
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# read the SVG file
doc = minidom.parse(vectorFile)
path_data = [[path.getAttribute('style'),path.getAttribute('d')] for path in doc.getElementsByTagName('path')]
doc.unlink()

#transfer to map editor (BLOODY HELL PAST SOUP WHAT WERE YOU THINKING WE NEED THESE)
editor = ximsa.MapEditor(mapFile)
for path_style,path_string in path_data:
    path = parse_path(path_string)
    fill = getPathStyleAttribute(path_style,'fill')
    if not (str(fill).startswith('#') and len(str(fill)) == 7):
      print('fill-debug:\n\tfill = {}\n\tpath_style = {}\n\tpath_string = {}'.format(fill,path_style,path_string))
      fill = 'none'
    if fill == 'none':pass
    else:       
        blockrgbfill = tuple(int(str(fill).strip('#')[i:i+2], 16) for i in (0, 2, 4)) + (1,)
        workingBlock = ximsa.Block(blockname,blockrgbfill,blocksurface,blockteamid,blockflags,blockterrain,[])

        for e in path:
            coords = []
            if isinstance(e, Move):   
                coords = [e.start.real,e.start.imag,0]
                workingBlock.nodes.append(ximsa.Node(coords))

            elif isinstance(e, Line):
                coords = [e.end.real,e.end.imag,0]
                workingBlock.nodes.append(ximsa.Node(coords))               

            elif isinstance(e, CubicBezier):
                x0 = e.start.real
                y0 = e.start.imag
                a0 = e.control1.real
                b0 = e.control1.imag
                x1 = e.end.real
                y1 = e.end.imag
                a1 = e.control2.real
                b1 = e.control2.imag
                points = [[x0,y0],[a0,b0],[a1,b1],[x1,y1]]

                #regulate number of nodes on small curves
                global distance_list
                distance_list = []
                for c,d in itertools.combinations(points, 2):
                    distance_list.append(np.sqrt((c[0]-d[0])**2+(c[1]-d[1])**2))
                step = .2 if max(distance_list) < 2 else .1
                    
                for t in reversed(np.arange(0, 1, step)):
                    coords = get_cubic_bezier_point(t, points) + [0]
                    workingBlock.nodes.append(ximsa.Node(coords))
                    
            elif isinstance(e, Close): pass
            else: print('path-debug:\n\t',e)

        editor.blocks.append(workingBlock)
editor.save()

#need to check if svg.path includes transformations in the path coordinates(translations?)
