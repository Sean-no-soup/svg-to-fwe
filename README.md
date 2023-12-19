# SVG to FWE converter

  **THIS IS STILL A WORK IN PROGRESS; INCOMPLETE. USE AT YOUR OWN RISK**
 - Sean-no-soup@gmail.com
 - [Discord](https://discord.gg/bHYWvVGRrF) 

I wanted to be able to do the gruntwork of designing terrain for forts 
(either for actual game-look-nice purposes or for utter meme abominations) 
in something more forgiving and efficient than the forts map editor. 

since forts maps format .fwe (forts war environment) is already so close to vector formats 
current focus has been on converting vector format .svg (scalable vector graphics) to .fwe. 

,and use .svg as a stepping stone for other formats
i.e. posterize and then trace boundarties of a raster image into vectors. this could also serve as a general map making library with tools for scripting shenanigans.




## Done
 - LINE-INATOR!!! convert curves and boxes to lines
 - STYLE-INATOR convert all the things into a .fwe friendly format of rgb line paths (but not yet transforms, clip paths, gradients,? )
 - preview in browser vectors
 - EXPORT to .FWE!

## planned features/functions/to-do
 - implement transforms from svg or
 - find a library that fucking works so I don't have to literally make a vector drawing and editing program from scratch
 - limit node count somewhat better
 - basic ui (probably still terminal)
 - helper theme for tiling, textures, props? wait, where are props saved (stay on task soup)

 
Release!?
 
 - scour handling
 - fix and add option to set terrain flags
 - normalize scale of svg to worldbounds
 - default improved limit node count
 - option to use color to set team of terrain blocks
 - gradient approximations
 - clip-paths handling
 - better ui
 - terrain auto tile (split terrain to use 1 of n^2 subtiles)
 - automate setup of certain scripting shenanigans (depending on what is actually scriptable I have some horrendous ideas for this like fake moving terrain)
   
 - incorporate destructible terrain script, make it work on hex or a randomized script
 - option to attempt removal of degenerate block areas (0-width, spindly artifacts of trace. ect)

 
## Installing (I don't recommend yet)
use the readme, further instruction posted here with releases

if you don't heed the warning it might be broken; good luck

## feedback, suggestions, help
PLEASE YES
[Discord](https://discord.gg/bHYWvVGRrF) 

## Change log
**0.2.2**
- transforms.... very broken, again (this is driving me up a wall)

**0.2.1**
- improved preview
- fixed degenerate nodes and disconinuities on curve approximations

**0.2.0**
- export to .fwe fixed and re-enabled
- fixed color

**0.1.2**
 - style-inator and line-inator per-path in prep()

**0.1.1**
 - clearer handling of missing dependencies because i feel like windette
 - line-inator
 - browser preview of path elements
 - export to fwe disabled (commented out so I can work on stuff that's broken)

**0.1.0**
 - kinda functioning for simple af .svg files but very limited, github pre-release

