#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:import map_editor as ximsa
except:input("missing dependency: ximsa's map editor")
try:import os
except:input('missing dependency: os')
try:import itertools
except:input('missing dependency: itertools')
try:import numpy as np
except:input('missing dependency: numpy\n\thttps://pypi.org/project/numpy/\n\tpip install numpy')
try:import svgpathtools as svgt
except:input('missing dependency: svgpathtools\n\thttps://pypi.org/project/svgpathtools/\n\tpip install svgpathtools')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions
def getVectorFile():
  listVectorFile = []
  for file in os.listdir():
    if file.endswith(".svg") : listVectorFile.append(file)
  assert len(listVectorFile) > 0, "'.svg' Vector file not found"
  print('\nwhich vector file?')
  for n in range(len(listVectorFile)):
      print('   {}:{}'.format(n,listVectorFile[n]))
  vectorFile = listVectorFile[int(input())]
  return vectorFile
      
def getMapFile():
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
    
def line_inator(paths): #indexing issues!, list path elements per path that aren't lines, replace from there using methods######
  '''makes all non-line path elements in paths entered into line approximations'''
  print('line-inating')#wow this library has everything!
  step = 0.2
  for path in paths:
    
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
        
  print('line-inated paths into.... lines')

def dict_path_attribute(pathAttributes,attribute = 'style'):
   return dict(i.split(':') for i in pathAttributes[0][attribute].split(';'))

def yn(text):
    if text.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:return True
    return False
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Classes

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#if __name__ = main:
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get svg data into python
vectorFile = getVectorFile()
svgPaths, svgPathsAttributes, svgAttributes = svgt.svg2paths2(vectorFile)


line_inator(svgPaths)
svgt.disvg(svgPaths)

###////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###get/set some map/block variables for constructing the fwe
##
##blockFlags = 0
##blockSurface = ''
##blockTerrain = "ui/textures/FE-Panel.tga"
##blockName = 'block' #'' if yn(input('flag terrain to not be destructible (when used with destructable terrain mod) (y/n)?\n')) else 'a' ###############################################
##blockTeamId = 3#int(input('terrain team?\n   1:team 1\n   2:team 2\n   3:any team\n   4:no team\n   5:background\n'))##################################################################
##flags = [ #terrain flags
##     ximsa.Flags.WindFloor,
##     ximsa.Flags.ViewFloor,
##     ximsa.Flags.NoDraw,
##     ximsa.Flags.Foundations,
##     ximsa.Flags.Mines,
##     ximsa.Flags.OilDrills,
##     ximsa.Flags.OilRigs,
##     ximsa.Flags.PassProjectiles,
##     ximsa.Flags.PassBeams,
##     ximsa.Flags.Hazard,
##     ximsa.Flags.NoSplash,
##     ximsa.Flags.NoBuild]
##
##for n in range(12):
##    #print('{} (y/n)?'.format(str(ximsa.Flags.readable(flags[n]))))
##    #flagbool = yn(input())  for the sake of testing things #############################################################################################################################
##    flagbool = False
##    if flagbool: blockflags = ximsa.Flags.set(blockflags, flags[n])
##
###////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###confirm
##'''
##print("add the vectors in {} to the file '{}' \nteam {} with flags{}, \nand blocks named '{}'\n(y/n)?\n".format(vectorFile,mapFile,blockTeamId,ximsa.Flags.readable(blockFlags),blockName),end = '')
##if not yn(input()):
##  print('exit')
##  quit####################################################################################################################################################################################
##'''
##
###////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###transfer to map editor (BLOODY HELL PAST SOUP WHAT WERE YOU THINKING WE NEED THESE)
###editor = ximsa.MapEditor(mapFile) #fwe constructor (filename, block list, save)
##
###convert non-line segments to lines
##
##
##
##
##'''
##for i in range(len(paths)):             #for each path i
##    path = paths[i]
##    style = getPathAttribute(pathsAttributes[i],'style')  
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
##'''


