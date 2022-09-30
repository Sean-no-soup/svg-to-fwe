#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:import map_editor as ximsa
except:input("missing dependency: ximsa's map editor")
try:import os
except:input('missing dependency: os')
##try:import itertools
##except:input('missing dependency: itertools')
##try:import tkinter as tk
##except:input('missing dependency: tkinter') 
try:import numpy as np
except:input('missing dependency: numpy\n\thttps://pypi.org/project/numpy/\n\tpip install numpy')
try:import svgpathtools as svgt
except:input('missing dependency: svgpathtools\n\thttps://pypi.org/project/svgpathtools/\n\tpip install svgpathtools')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions
def hex_to_rgb_1(hexString):
  return tuple(int(hexString.strip('#')[i:i + 2], 16)/255 for i in range(0, 6, 2))+(1.0,)

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
#get svg data into python, prep for export
vectorFile = get_vector_file()
mapFile = get_map_file()

svgPaths, svgPathsAttributes, svgAttributes = svgt.svg2paths2(vectorFile)

prep()


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

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#confirm
svgt.disvg(svgPaths,filename = 'SVGtoFWEpreview.svg',attributes = svgPathsAttributes)
print("\nadd the vectors in {} to the file '{}' \nteam {} with flags{}, \nand blocks named '{}'\n(y/n)?\n".format(vectorFile,mapFile,blockTeamId,ximsa.Flags.readable(blockFlags),blockName),end = '')
if not yn(input()):
  print('exit')
  quit


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#transfer to map editor (BLOODY HELL PAST SOUP WHAT WERE YOU THINKING WE NEED THESE)
editor = ximsa.MapEditor(mapFile) #fwe constructor (filename, block list, save)

for i in range(len(svgPaths)):             #for each path i
    path = svgPaths[i]
    fill = svgPathsAttributes[i]['fill']

    if fill == 'none':pass
    else:       
        blockRGBFill = hex_to_rgb_1(fill)
        
        workingBlock = ximsa.Block(blockName,blockRGBFill,blockSurface,blockTeamId,blockFlags,blockTerrain,[])

        for e in path:  #for each path element
          
            if isinstance(e, svgt.path.Line):   
                workingBlock.nodes.append(ximsa.Node([e.start.real,e.start.imag,0]))
            
            else: print('path-debug:\n\t',type(e),'\n\t',e,'\n')

        editor.blocks.append(workingBlock)
        
editor.save()


