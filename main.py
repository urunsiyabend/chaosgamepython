# Example file showing a basic pygame "game loop"
import math
import random

import pygame
import argparse

from barnsley_fern import BarnsleyFern
from graphics import GraphicDrawer, PygameGraphicDrawer
from sierpinski import SierpinskiTriangleConfig, SierpinskiTriangle

# parse command line arguments
parser = argparse.ArgumentParser(description="Sierpinski Triangle")
parser.add_argument("--fullscreen", action="store_true", help="Run in fullscreen mode")
parser.add_argument("--max-iteration-count", type=int, help="Maximum iteration count")
parser.add_argument("--triangle", type=int, nargs=6, help="Triangle coordinates (x1, y1, x2, y2, x3, y3)")
parser.add_argument("--border-color", type=str, help="Border color of triangle")
parser.add_argument("--fill-color", type=str, help="Fill color of triangle")
parser.add_argument("--border-width", type=int, help="Border width of triangle")
parser.add_argument("--dot-color", type=str, help="Dot color")
args = parser.parse_args()

# set fullscreen mode
fullscreen = args.fullscreen

# set screen width and height
screen_width = 1280
screen_height = 800

# set screen caption
screen_caption = "Barnsley Fern"

# # create triangle
# triangle = [(screen_width // 2, 100), (200, screen_height - 100), (screen_width - 200, screen_height - 100)]
# triangle_config = SierpinskiTriangleConfig(triangle, "white", 1, 10 ** 6, "red")
# sierpinski_triangle = SierpinskiTriangle(triangle_config)

# create_barnsley_fern
barnsley_fern = BarnsleyFern(0, 0)


# setup pygame
drawer: GraphicDrawer = PygameGraphicDrawer(barnsley_fern, screen_width, screen_height, fullscreen, screen_caption)

# draw
drawer.draw()



pygame.quit()
