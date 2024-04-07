#DOM: document-object-model, representation of an xml document
#XML: extensible-markup-langieage, rules to define data, cannot persorm operations by itself
#SVG: scalable-vector-graphics, xml vector image format
#FWE: forts-war-environment, map format for forts, terrain used a format like svg but only lines

import xml.dom
#most powerful
#https://docs.python.org/3/library/xml.dom.html

import xml.dom.minidom
#minimal implementationn smaller than dom
#https://docs.python.org/3/library/xml.dom.minidom.html#module-xml.dom.minidom 

import xml.etree.ElementTree
#simple api for dom, reccomended for new users doing xml processing
#https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree