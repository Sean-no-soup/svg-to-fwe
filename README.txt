---------------------------------------------------------------------------------------------------
NEED 
-PYTHON (duh)
-Modules/dependencies (depend on version but span):
	Ximsa's map editing library
		matplotlib
		math
		struct
		sys
	os                          (included in standard python utility modules)
	numpy                       https://numpy.org/install/                          pip install numpy
	itertools                   https://docs.python.org/3/library/itertools.html    pip install more-itertools	
	sv.path                     https://github.com/regebro/svg.path   
	

---------------------------------------------------------------------------------------------------
Some helpful tools
https://www.autotracer.org/
	is free but janky, unsure how useful this would be for mapping, be careful of complex stuff

https://inkscape.org/
	for more detailed design stuff, more complex functions may not be supported when converting
---------------------------------------------------------------------------------------------------

map_editor.py and the svg-to-fwe.py must be in the same directory

---------------------------------------------------------------------------------------------------
AT THIS TIME ONLY VECTORS WITH FILL WILL BE INCLUDED, 
GRADIENT FILLS ARE CURRENTLY IGNORED, CLIP PATHS ARE DISABLED,
SOME TRANSFORM FUNCTIONS ARE BROKEN
STROKE WIDTH DOES NOT HAVE ANY EFFECT. 