---------------------------------------------------------------------------------------------------
REQUIREMENTS/INSTALLATION (0.2.0)
-python3

-Modules/dependencies:
	ximsa's map editor (included)
	
	os (python default module)
	
	numpy 
		https://pypi.org/project/numpy/ 
		pip install numpy
		
	svgpathtools 
		https://pypi.org/project/svgpathtools/ 
		pip install svgpathtools
		
-in the same directory (folder)
	svg-to-fwe-0.2.0.py
	map_editor.py
	<vector file you want to use>.svg
	
'run 'svg-to-fwe-0.2.0.py'
---------------------------------------------------------------------------------------------------
Some helpful tools
https://www.autotracer.org/
	is free but janky, unsure how useful this would be for mapping, be careful of complex stuff

https://inkscape.org/
	for more detailed design stuff, more complex functions may not be supported when converting
---------------------------------------------------------------------------------------------------
WARNING
-Many more advanced features of the svg format cannot be faithfully recreated withing the limitations of a forts war environment. work to approximate things such as gradients is ongoing but will take a while.

-gradients are currently replaced with fill=#000000
-svg path transforms aren't implemented yet
---------------------------------------------------------------------------------------------------
SUPPORT/FEATURE REQUEST/ECT:
-  https://discord.gg/bHYWvVGRrF  -  Sean, no soup#5766  -
