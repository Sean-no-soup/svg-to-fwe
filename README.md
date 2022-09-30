# SVG to FWE converter

  **THIS IS STILL A WORK IN PROGRESS; INCOMPLETE. USE AT YOUR OWN RISK**
 - Sean-no-soup@gmail.com
 - [Discord](https://discord.gg/bHYWvVGRrF) 
 ## Features
 - LINE-INATOR!!! convert curves to lines (fwe only uses lines)
 - STYLE-INATOR (rudimentarally convert attributes, including embeded css-style, to necessary attributes for export. sets gradients to #000000 and clip paths to no fill) 
 - preview in browser vectors
 - EXPORT to .FWE!

## planned features/functions/to-do
 - implement transforms from svg 
 - limit node count
 
Release!

 - fix and add option to set terrain flags
 - normalize scale of new blocks
 - default option to limit/change node count on small radii
 - option to use color to set team of terrain blocks
 -
 - gradient approximations
 - clip-paths
 
 - incorporate destructible terrain script
 - option to attempt removal of degenerate block areas (0-width, spindly artifacts of trace. ect)
 
 - - if __name__ == "__main__": so functions could be used as a library (but with svgpathtools is that needed?, perhaps to implement a gui)
 
## Installing (don't yet)
use the readme, further instruction posted here with releases

might be broken; good luck

## feedback, suggestions, help
PLEASE YES
[Discord](https://discord.gg/bHYWvVGRrF) 

## Change log
**0.2.1**
- improved preview
- fixed degenerate nodes and disconinuities on curve approximations
- 

**0.2.0**
- export to .fwe fixed and re-enabled
- fixed color

**0.1.2**
 - style-inator and line-inator per-path in prep()

**0.1.1**
 - clearer handling of missing dependencies
 - line-inator
 - browser preview of path elements
 - export to fwe disabled

**0.1.0**
 - kinda functioning but very limited, github pre-release

