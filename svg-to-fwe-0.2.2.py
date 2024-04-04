#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:import map_editor as ximsa
except ImportError:input("missing dependency: ximsa's map editor, how did you get this and not the map editor")
try:import os
except ImportError:input('missing dependency: os')
##try:import itertools
##except ImportError:input('missing dependency: itertools')
##try:import tkinter as tk
##except ImportError:input('missing dependency: tkinter') 
try:import numpy as np
except ImportError:input('missing dependency: numpy\n\thttps://pypi.org/project/numpy/\n\tpip install numpy')
try:import svgpathtools as svgt
except ImportError:input('missing dependency: svgpathtools\n\thttps://pypi.org/project/svgpathtools/\n\tpip install svgpathtools')
try:from scour.scour import start as scour, parse_args as scour_args, getInOut as scour_io
except ImportError:input('missing dependency: scour\n\thttps://pypi.org/project/scour//\n\tpip install scour')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions
def yn(text):
    if text.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:return True
    return False

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

def scour_svg(infilename):
  '''scour the input.svg, save to script directory, and return output.svg'''
  outfilename = infilename.strip('.svg')+'scoured.svg'
  options = scour_args()
  options.infilename = infilename
  options.outfilename = outfilename
  # Set options here or accept defaults.
  (input, output) = scour_io(options)
  scour(options, input, output)
  return outfilename

def hex_to_rgb_1(hexString):
  '''return rgba 0-1 used for for map editor format'''
  return tuple(int(hexString.strip('#')[i:i + 2], 16)/255 for i in range(0, 6, 2))+(1.0,)

def line_inator(path): 
  '''in place approximate all non-line path elements in a path'''

  step = 0.2
  issueIndexes = []

  for i in range(len(path)):          #make a list of indexes for all non-line elements
    pathElement = path[i]
    if type(pathElement) != svgt.path.Line:
      issueIndexes.append(i)
  if len(issueIndexes) > 0:
    
    for i in issueIndexes[::-1]:      #go through all non-line elements
      coords = list(path[i].point(t) for t in reversed(np.arange(0, 1.1, step))) #take coordinates along the non-line element
      prevStart = path[i].start
      prevEnd = path[i].end
      
      path.remove(path[i])            #replace non-line element with line elements between the coordinates from before
      for j in range(len(coords)-1): 
        path.insert(i,svgt.Line(start = coords[j+1], end = coords[j]))
        if j == 0:path[i].end = prevEnd
      path[i].start = prevStart
    
  return

def transform_inator(pathAttributes,paths,index): 
  ''' transform path in place, replace coordinates+transform with transformed coordinates,
    there's an argument to move all this to export/to-map-editor step due to interaction with style_inator and path attributions'''

  if 'transform' in pathAttributes: #assuming for now that svgt or scour only gives 0-1 transform (I haven't seen any example to the contrary yet)
 
    type_str, value_str = pathAttributes['transform'].split('(')
    value_str = value_str.replace(',', ' ')
    value_str = value_str.replace(')', '')
    print('transforminator value string',value_str)
    values = list(map(float, filter(None, value_str.split(' '))))
    print(values)
    
    if type_str == 'scale' :
      if len(values) == 1: values.append(values[0]) #?????????????????????????????????why is this necessary
      paths[index] = svgt.path.scale(paths[index],values[0],values[1])

    elif type_str == 'rotate' : #rotate occasionally specifies 3 values. mozilla docs says 1(for rotate) or 4 (for rotate3d()). ?????????????????????????????????
      if len(values) > 1: print('--rotate values debug--',values)
      paths[index] = svgt.path.rotate(paths[index],values[0])

    elif type_str == 'translate' :#working?
      paths[index] = svgt.path.translate(paths[index],values[0]+values[1]*0j)

    elif type_str == 'matrix' :#oh no please help
      try:paths[index] = svgt.path.transform(paths[index],svgt.parser.parse_transform(pathAttributes['transform'])) #(this occasionally breaks for arcs.indicates probably not correct (idk if this is the only problem but it doesn't seem sufficient to cause the big problems?
      except:print('----------------------------',pathAttributes['transform'],paths[index],'----------------------------',sep = '\n')  

def style_inator(pathsAttributes,index):
  '''in place set a path's attributes for export and preview

current:
  fill = #rrggbb 
    -from fill or from style if found
    -gradients set to #000000 ##### this could also be a problem for transparancies.... oh no
    -default to None (clip paths and other)
  stroke = #000000
  stroke-width = 0.1 

  truncates any other attributes (will have to come AFTER transforms or be updated)
'''
  pathAttributes = pathsAttributes[index]

  fill = 'none' 
  if 'fill' in pathAttributes:
    fill = str(pathAttributes['fill'])
  elif 'style' in pathAttributes:
    styleDict = dict(i.split(':') for i in pathAttributes['style'].split(';'))
    if 'fill' in styleDict: fill = styleDict['fill']
    else:fill = 'none'
  elif 'Gradient' in fill: fill = '#000000'
  
  pathsAttributes[index] = {'fill':fill,'stroke':'#000000','stroke-width':'0.1'}
  return




  ##    transform = svgt.parser.parse_transform(pathAttributes['transform']) #I really wanted this to work, but the transform matrix returned when applies does not center the transform the same as above tested with rotations
  ##    print(transform)
  ##    print(paths[index]) 
  ##    print(pathAttributes['transform']) #as stored
  ##    print(svgt.parser.parse_transform(pathAttributes['transform'])) #matrix
  ##    try:
  ##      path = svgt.path.transform(paths[index],transform)
  ##      paths[index] = path
  ##    except:
  ##      print('----------------------------------------------------------------------------------------------------')
  ##      print(paths[index],'\n',pathAttributes['transform'],'\n',svgt.parser.parse_transform(pathAttributes['transform']))
  '''
  CSS transforms https://www.w3schools.com/cssref/css3_pr_transform.asp and number of parameters

  matrix            6
  matrix3d          16
  
  translate         2
  translate3d       3
  translate x,y,z   1 each

  scale             2
  scale3d           3
  scalex,y,z        1 each

  rotate            1
  rotate3d          4
  rotatex,y,z       1 each

  skew              2
  skew x,y          1 each

  perspective       1

  inherit           FROM PARENT ELEMENT
  '''
  #set transform attribute to none?
  return

def debug_transforms():
  '''take each path, and its 'transformed' variant and put them into the same svg named according to the transform'''
  pass

def prep():
  '''
  set everything up for export/preview
  '''
## transform -> style -> lines (style must be after transform but line_inator order? 
# before to simplify transforms (by only working with line elements)
# or after to not fuss with transforms?

  paths = svgPaths
  pathsAttributes = svgPathsAttributes
  
  for i in range(len(svgPaths)):
    
    transform_inator(pathsAttributes[i],paths,i)
    
    style_inator(pathsAttributes,i)

    line_inator(paths[i])
    
  return

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Classes

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get svg data into python, prep for export

#vectorFile = scour_svg(get_vector_file())
vectorFile = get_vector_file()

svgPaths, svgPathsAttributes, svgAttributes = svgt.svg2paths2(vectorFile)

#mapFile = get_map_file() #############################################################################################################################################################################

#prep()
print(svgAttributes)
svgt.disvg(svgPaths,filename = 'SVGtoFWEpreview.svg',attributes = svgPathsAttributes)























'''
#####################################################################################################################################################################################################################
#the rest *should* work if the preview works but I don't need to run it

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#get/set some map/block variables for constructing the fwe

blockFlags = 0
blockSurface = ''
blockTerrain = "ui/textures/FE-Panel.tga"
blockName = 'block' #'' if yn(input('flag terrain to not be destructible (when used with destructable terrain mod) (y/n)?\n')) else 'a' 
blockTeamId = 3#int(input('terrain team?\n   1:team 1\n   2:team 2\n   3:any team\n   4:no team\n   5:background\n'))
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

for n in range(12): #ask user what properties to assign blocks
    #print('{} (y/n)?'.format(str(ximsa.Flags.readable(flags[n]))))
    #flagbool = yn(input()) 
    flagbool = False #no to all properties########################################################################################################################################################################################################
    if flagbool: blockflags = ximsa.Flags.set(blockflags, flags[n])

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###confirm
svgt.disvg(svgPaths,filename = 'SVGtoFWEpreview.svg',attributes = svgPathsAttributes) #preview

##print("\nadd the vectors in {} to the file '{}' \nteam {} with flags{}, \nand blocks named '{}'\n(y/n)?\n".format(vectorFile,mapFile,blockTeamId,ximsa.Flags.readable(blockFlags),blockName),end = '')
##if not yn(input()):################################################################################################################################################################################################################################################
##  quit

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#transfer to map editor and .fwe
editor = ximsa.MapEditor(mapFile)           #fwe constructor (filename, block list, save)

for i in range(len(svgPaths)):              #for each path and its fill
    path = svgPaths[i]                      
    fill = svgPathsAttributes[i]['fill']

    if fill != 'none':       
        blockRGBFill = hex_to_rgb_1(fill)   #if there's a fill set up a new block 
        
        workingBlock = ximsa.Block(blockName,blockRGBFill,blockSurface,blockTeamId,blockFlags,blockTerrain,[])

        for e in path:                      #construct block
          
            if isinstance(e, svgt.path.Line):   
                workingBlock.nodes.append(ximsa.Node([e.start.real,e.start.imag,0]))
            
            else: print('path debug in block constructor:\n\t',type(e),'\n\t',e,'\n')

        editor.blocks.append(workingBlock)
        
editor.save()
'''