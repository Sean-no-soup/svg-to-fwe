#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import map_editor as ximsa
import os
import numpy as np
import svgpathtools as svgt
from scour.scour import start as scour, parse_args as scour_args, getInOut as scour_io
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#functions
def yn(text):
    if text.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:return True
    return False

def get_svg_file(string = ''):
  listVectorFile = []
  for file in os.listdir():
    if file.endswith(".svg") : listVectorFile.append(file)
  assert len(listVectorFile) > 0, "'.svg' Vector file not found"
  if string == '':print('\nwhich vector file?')
  else:print('\nwhich vector file for {}?'.format(string))
  for n in range(len(listVectorFile)):
      print('   {}:{}'.format(n,listVectorFile[n]))
  vectorFile = listVectorFile[int(input())]
  return vectorFile
      
def get_fwe_file():
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
  outfilename = infilename.strip('.svg')+'scoured.svg'
  options = scour_args()
  options.infilename = infilename
  options.outfilename = outfilename
  # Set options here or accept defaults.
  (input, output) = scour_io(options)
  scour(options, input, output)
  return outfilename

def hex_to_rgb_1(hexString):
  '''rgba 0-1 for map editor format'''
  return tuple(int(hexString.strip('#')[i:i + 2], 16)/255 for i in range(0, 6, 2))+(1.0,)

def line_inator(path): #indexing issues!, list path elements per path that aren't lines, replace from there using methods######
  '''approximate non-line path elements in place'''
  step = 0.2
  issueIndexes = []
  for i in range(len(path)):#list indexes of non-lines in current path
    pathElement = path[i]
    if type(pathElement) != svgt.path.Line:
      issueIndexes.append(i)
  if len(issueIndexes) > 0:
    
    for i in issueIndexes[::-1]: #end to beginning of path to avoid indexing issues, index of each non-line element
      coords = list(path[i].point(t) for t in reversed(np.arange(0, 1.1, step))) #coords along issue element, end to beginning
      prevStart = path[i].start
      prevEnd = path[i].end
      
      path.remove(path[i])
      for j in range(len(coords)-1): #replace now missing element with lines from the prior end to start, again to avoid indexing issues
        path.insert(i,svgt.Line(start = coords[j+1], end = coords[j]))
        if j == 0:path[i].end = prevEnd
      path[i].start = prevStart
  return
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def style_inator(pathsAttributes,index):
  '''set attributes for export/preview
current:
  fill = #rrggbb (from fill or from style)
    -default to None if not defined in either(clip paths, anything else?)
    -gradients set to #000000 ########################################################################## this could also be a problem for transparancies.... oh no

    fill, default stroke and stroke-width for preview. clips any others
'''
  pathAttributes = pathsAttributes[index]
  if 'fill' in pathAttributes:
    fill = str(pathAttributes['fill'])
  elif 'style' in pathAttributes:
    styleDict = dict(i.split(':') for i in pathAttributes['style'].split(';'))
    if 'fill' in styleDict: fill = styleDict['fill']
    else:fill = 'none'
  else:fill = 'none'
  
  if 'Gradient' in fill: fill = '#000000'
  
  pathsAttributes[index] = {'fill':fill,'stroke':'#000000','stroke-width':'0.1'}
  return

def transform_inator(pathAttributes,paths,index): #argument to bake into export, this may fuck with gradients######################################
  ''' transform path in place, transform attribute redundant ''' 
  if 'transform' in pathAttributes: #assuming for now that svgt or scour only gives 1 transform (I haven't seen any example to the contrary yet
 
    type_str, value_str = pathAttributes['transform'].split('(')
    value_str = value_str.replace(',', ' ')
    value_str = value_str.replace(')', '')
    values = list(map(float, filter(None, value_str.split(' '))))
    
    if type_str == 'scale' :
      if len(values) == 1: values.append(values[0])
      paths[index] = svgt.path.scale(paths[index],values[0],values[1])
    elif type_str == 'rotate' :
      if len(values) > 1: print('rotate',values) #rotate occasionally specifies 3 values. mozilla docs says 1(for rotate) or 4 (for rotate3d()). 
      paths[index] = svgt.path.rotate(paths[index],values[0])
    elif type_str == 'translate' :
      paths[index] = svgt.path.translate(paths[index],values[0]+values[1]*0j)
    elif type_str == 'matrix' :
      try:paths[index] = svgt.path.transform(paths[index],svgt.parser.parse_transform(pathAttributes['transform'])) #(this occasionally breaks for arcs.indicates probably not correct (idk if this is the only problem but it doesn't seem sufficient to cause the big problems?
      except:print('----------------------------',pathAttributes['transform'],paths[index],'----------------------------',sep = '\n')  
    
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
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

svf = "pntfunniscoured.svg"
svgPaths, svgPathsAttributes, svgAttributes = svgt.svg2paths2(svf)
svgt.disvg(svgPaths,filename = 'transform test.svg',attributes = svgPathsAttributes, svg_attributes = svgAttributes)

##svfr =  "log scale originscoured.svg"

##svgrPaths, svgrPathsAttributes, svgrAttributes = svgt.svg2paths2(svfr)

##svgrAttributes['width'] = svgAttributes['width']
##svgrAttributes['height'] = svgAttributes['height']
##svgrAttributes['viewBox'] = svgAttributes['viewBox']



##print(svgAttributes,'\n\n',svgrAttributes)

'''{
'xmlns': 'http://www.w3.org/2000/svg',
'xmlns:cc': 'http://creativecommons.org/ns#',
'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
'xmlns:xlink': 'http://www.w3.org/1999/xlink',
'id': 'svg8',
'width': '210mm',
'height': '297mm',
'version': '1.1',
'viewBox': '0 0 210 297'} 
'''


##for i in range(len(svgPaths)):
    #construct paths and attributes? paths. plural? not sure how this library will take it
    #preview original and transform
##    for pathElement in svgPaths[i]:
##        print(pathElement)
##
##    for attribute in svgPathsAttributes[i]:
##        if attribute in ('transform','x','y','width','height'):
##            print(attribute,':',svgPathsAttributes[i][attribute])
            

##    print("####################################################################################################################################################")
    
##    
##    svgt.disvg(\
##        svgPaths,\
##        filename = 'SVGtoFWEpreview.svg',\
##        attributes = svgPathsAttributes)\
##
##    if input()!= '':
##        #details
##
##go through an svg
##
##for each path, to cyle through on viewer command
##    export explicit transform against a reference (just export that path)
##    transform to implicit transform and export a preview against a reference
##
##    if requested in this loop, export all path data for each
##
##




















































'''
for pathAttributes in svgPathsAttributes:
	for attribute in pathAttributes:
		if attribute not in list2:list2.append(attribute)
['d',

 'id',
 
 'style',
 'class',
 'transform',

 'clip-path',
 
 'cx','cy', center points
 'rx','ry', radii on axis
 'r', radius of a circle
 
 'x', 'y', coords in the 'user coord system' 
 'width', length in user coord system 
 'height', length in user coord system

'''
'''
transform

none https://www.w3schools.com/cssref/css3_pr_transform.asp
matrix
matrix3d
translate
translate3d
translate x,y,z
scale
scale3d
scalex,y,z
rotate
rotate3d
rotatex,y,z
skew
skew x,y
perspective

initial
inherit
'''
