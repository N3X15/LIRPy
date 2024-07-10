# LIRPy

Largest Interior Rectangle for Python

The purpose of LIRPy was to originally to find the largest rectangle that can fit within the shape defined by a 2D boolean grid.  It can also repeat this operation until the mask is completely represented by a list of successively smaller rects. In short, this library can cut up shapes into rectangles.

LIRPy has now evolved into providing a framework for not just 2D rectangles, but also 3D cuboids in a 3D boolean grid.

This was originally made for a stupid Minecraft project for the purpose of making as few Baritone selections as possible when designating a cylinder, but it can now generate efficient baritone selections for entire facilities.

I also hate numpy with a passion for mysterious reasons I can't even explain to myself.  Therefore, this project doesn't use it.

## Background

When I'm not breaking games for work, I tend to play engineering games, and one of the first such games I got into was Minecraft.  I play it off and on, and I tend to get into mega-projects, which often end up with me getting bored and having a bot called Baritone do most of the work. 

I needed a tool to generate Baritone selection AABBs (which are defined by opposing corner coordinates) for cylinders of arbitrary radius and depth. The easiest possible way would be to generate selections for every single voxel column.  This would not be practical due to the sheer number of selections needing to be made.

So, after doing some research, I determined what I needed was an axis-aligned largest interior rectangle library.

## Other Options

Other solutions I've looked at:

* [largestinteriorrectangle](https://github.com/lukasalexanderweber/lir) uses numba, which is so outdated it won't compile with LLVM 14.  It's also unfortunately spammed all over stackoverflow, which makes it harder to find background information.
* https://www.evryway.com/largest-interior/ - Never worked properly for me.
* https://pypi.org/project/maxrect/ - GIS-specific, so it requires weird inputs and works on polygons rather than grids. Their GitHub is also missing.
* Various things in other languages, like C, MATLAB, and C# - no

So I made my own system, with blackjack and classy sex workers.

## Caveats

I am no mathematician, so this is nowhere within ten light-years of optimized, and there are probably a dozen papers dense with calculus describing new and exciting ways of doing that. I didn't take calculus in uni.

This works well enough for my purposes, but **PRs with improvements are absolutely welcome.**

## Installation

Requires Python >= 3.10

`pip install lirpy`

## Development

Requires Python >= 3.10 *and* `poetry`

## Example:
```shell
lirpy --x=-485 --y=40 --z=596 --output-type=baritone --dump-steps circle -r 7
```
```
Center: -485 40 596
Outer Radius: 7
Inner Radius: 0
Depth: 0
Along axis: -Y
Step 0:
       █       
    ███████    
   █████████   
  ███████████  
 █████████████ 
 █████████████ 
 █████████████ 
███████████████
 █████████████ 
 █████████████ 
 █████████████ 
  ███████████  
   █████████   
    ███████    
       █       
Step 1:
       █       
    ███████    
               
  █         █  
 ██         ██ 
 ██         ██ 
 ██         ██ 
███         ███
 ██         ██ 
 ██         ██ 
 ██         ██ 
  █         █  
               
    ███████    
       █       
Step 2:
       █       
    ███████    
               
  █         █  
            ██ 
            ██ 
            ██ 
█           ███
            ██ 
            ██ 
            ██ 
  █         █  
               
    ███████    
       █       
Step 3:
       █       
    ███████    
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
    ███████    
       █       
Step 4:
       █       
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
    ███████    
       █       
Step 5:
       █       
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 6:
               
               
               
  █         █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 7:
               
               
               
            █  
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 8:
               
               
               
               
               
               
               
█             █
               
               
               
  █         █  
               
               
       █       
Step 9:
               
               
               
               
               
               
               
              █
               
               
               
  █         █  
               
               
       █       
Step 10:
               
               
               
               
               
               
               
               
               
               
               
  █         █  
               
               
       █       
Step 11:
               
               
               
               
               
               
               
               
               
               
               
            █  
               
               
       █       
Step 12:
               
               
               
               
               
               
               
               
               
               
               
               
               
               
       █       
Step 13:
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
#sel clear
#sel 1 -489 40 591
#sel 2 -481 40 601
#sel 1 -491 40 593
#sel 2 -490 40 599
#sel 1 -480 40 593
#sel 2 -479 40 599
#sel 1 -488 40 590
#sel 2 -482 40 590
#sel 1 -488 40 602
#sel 2 -482 40 602
#sel 1 -485 40 589
#sel 2 -485 40 589
#sel 1 -490 40 592
#sel 2 -490 40 592
#sel 1 -480 40 592
#sel 2 -480 40 592
#sel 1 -492 40 596
#sel 2 -492 40 596
#sel 1 -478 40 596
#sel 2 -478 40 596
#sel 1 -490 40 600
#sel 2 -490 40 600
#sel 1 -480 40 600
#sel 2 -480 40 600
#sel 1 -485 40 603
#sel 2 -485 40 603
```

## Visualized
![javaw_2023-03-26_14-11-18](https://user-images.githubusercontent.com/110073/227816801-68ed2653-2cdf-454c-b901-9fb930d5fa23.png)

