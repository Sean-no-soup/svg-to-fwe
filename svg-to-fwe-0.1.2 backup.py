#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:import map_editor as ximsa
except:input("missing dependency: ximsa's map editor")
try:import os
except:input('missing dependency: os')
try:import itertools
except:input('missing dependency: itertools')
##try:import tkinter as tk
##except:input('missing dependency: tkinter') 
try:import numpy as np
except:input('missing dependency: numpy\n\thttps://pypi.org/project/numpy/\n\tpip install numpy')
try:import svgpathtools as svgt
except:input('missing dependency: svgpathtools\n\thttps://pypi.org/project/svgpathtools/\n\tpip install svgpathtools')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions

def get_vector_file():
  listVectorFile = []
  for file in os.listdir():
    if file.endswith(".svg") : listVectorFile.append(file)
  assert len(listVectorFile) > 0, "'.svg' Vector file not found"
  print('\nwhich vector file?')
  for n in range(len(listVectorFile)):
      print('   {}:{}'.format(n,listVectorFile[n]))
  vectorFile = listVectorFile[int(input())]
  return vectorFile
      
def get_map_file():
  listMapFile = []
  for file in os.listdir():
    if file.endswith(".fwe") : listMapFile.append(file)
  print('which terrain file?\n   0:make a new file') 
  for n in range(len(listMapFile)):
    print('   {}:{}'.format(n+1,listMapFile[n]))
  terrain_choice = int(input())
  if terrain_choice == 0: mapFile = str(input('new map name:'))+'.fwe'
  else: mapFile = listMapFile[terrain_choice-1]
  return mapFile

def prep():
  paths = svgPaths
  pathsAttributes = svgPathsAttributes
  for i in range(len(svgPaths)):
    line_inator(svgPaths[i])
    style_inator(svgPathsAttributes,i)
  return
    
def line_inator(path): #indexing issues!, list path elements per path that aren't lines, replace from there using methods######
  '''NOT path-S. makes all non-line path elements in a path entered into line approximations'''
  step = 0.2
  issueIndexes = []
  for i in range(len(path)):#list indexes of non-lines in current path
    pathElement = path[i]
    if type(pathElement) != svgt.path.Line:
      issueIndexes.append(i)
  if len(issueIndexes) > 0:
    for i in issueIndexes[::-1]: #end to beginning of path to avoid indexing issues, index of each non-line element
      coords = list(path[i].point(t) for t in reversed(np.arange(0, 1.1, step))) #coords along issue element, end to beginning
      path.remove(path[i])
      for j in range(len(coords)-1): #replace now missing element with lines from the prior end to start, again to avoid indexing issues
        path.insert(i,svgt.Line(start = coords[j], end = coords[j+1]))
  return

def style_inator(pathsAttributes,index):
  '''NOT path-S attributes. from css-style (css-class will become a problem later) to workable modify in place for now
current:
          find pathAttributes -> fill
          -(default to None if not defined or in style. clip paths here are going to be hell)
          -gradients set to #000000
          default ->stroke, stroke-width
'''
  if 'style' in pathsAttributes[index]:
    fill = dict(i.split(':') for i in pathsAttributes[index]['style'].split(';'))['fill']
  elif 'fill' in pathsAttributes[index]:
    fill = str(pathsAttributes[index]['fill'])   
  else:fill = 'none'
  if 'Gradient' in fill: fill = '#000000'
  pathsAttributes[index] = {'fill':fill,'stroke':'#000000','stroke-width':'0.1'}
  return


def yn(text):
    if text.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:return True
    return False
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Classes

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#if __name__ = main: #do this first, then gui
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get svg data into python
vectorFile = get_vector_file()
svgPaths, svgPathsAttributes, svgAttributes = svgt.svg2paths2(vectorFile)

prep()
svgt.disvg(svgPaths,filename = 'test.svg',attributes = svgPathsAttributes)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get/set some map/block variables for constructing the fwe

blockFlags = 0
blockSurface = ''
blockTerrain = "ui/textures/FE-Panel.tga"
blockName = 'block' #'' if yn(input('flag terrain to not be destructible (when used with destructable terrain mod) (y/n)?\n')) else 'a' ###############################################
blockTeamId = 3#int(input('terrain team?\n   1:team 1\n   2:team 2\n   3:any team\n   4:no team\n   5:background\n'))##################################################################
flags = [ #terrain flags
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
    #flagbool = yn(input())  for the sake of testing things #############################################################################################################################
    flagbool = False
    if flagbool: blockflags = ximsa.Flags.set(blockflags, flags[n])

###////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###confirm
##
##print("add the vectors in {} to the file '{}' \nteam {} with flags{}, \nand blocks named '{}'\n(y/n)?\n".format(vectorFile,mapFile,blockTeamId,ximsa.Flags.readable(blockFlags),blockName),end = '')
##if not yn(input()):
##  print('exit')
##  quit####################################################################################################################################################################################
##

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#transfer to map editor (BLOODY HELL PAST SOUP WHAT WERE YOU THINKING WE NEED THESE)
#editor = ximsa.MapEditor(mapFile) #fwe constructor (filename, block list, save)

#convert non-line segments to lines




##
##for i in range(len(svgPaths)):             #for each path i
##    path = svgPaths[i]
##    print(svgPaths[i])
##    print(svgPathsAttributes[i])
##    #style = dict_path_attribute(svgPathsAttributes[i],'style') #PROBLEM  sometimes fill is an attributes, and sometimes style which contains fill
##    fill = style['fill']
##    print('fill:',fill)
##    print()
##    if not (str(fill).startswith('#') and len(str(fill)) == 7):
##      print('fill-debug:\n\tfill = {}\n\tpath_style = {}\n\tpath_string = {}'.format(fill,path_style,path_string))
##      fill = 'none'
##    if fill == 'none':pass
##    else:       
##        blockrgbfill = tuple(int(str(fill).strip('#')[i:i+2], 16) for i in (0, 2, 4)) + (1,)
##        workingBlock = ximsa.Block(blockname,blockrgbfill,blocksurface,blockteamid,blockflags,blockterrain,[])
##
##        for e in path:  #MOVE THIS TO WORKING PATH-ELEMENT CLASSES METHODS
##            coords = []
##            if isinstance(e, Move):   
##                coords = [e.start.real,e.start.imag,0]
##                workingBlock.nodes.append(ximsa.Node(coords))
##
##            elif isinstance(e, Line):
##                coords = [e.end.real,e.end.imag,0]
##                workingBlock.nodes.append(ximsa.Node(coords))               
##
##            elif isinstance(e, CubicBezier):
##                x0 = e.start.real
##                y0 = e.start.imag
##                a0 = e.control1.real
##                b0 = e.control1.imag
##                x1 = e.end.real
##                y1 = e.end.imag
##                a1 = e.control2.real
##                b1 = e.control2.imag
##                points = [[x0,y0],[a0,b0],[a1,b1],[x1,y1]]
##
##                #regulate number of nodes on small curves
##                global distance_list
##                distance_list = []
##                for c,d in itertools.combinations(points, 2):
##                    distance_list.append(np.sqrt((c[0]-d[0])**2+(c[1]-d[1])**2))
##                step = .2 if max(distance_list) < 2 else .1
##                    
##                for t in reversed(np.arange(0, 1, step)):
##                    coords = get_cubic_bezier_point(t, points) + [0]
##                    workingBlock.nodes.append(ximsa.Node(coords))
##                    
##            elif isinstance(e, Close): pass
##            else: print('path-debug:\n\t',e)
##
##        editor.blocks.append(workingBlock)
##editor.save()


