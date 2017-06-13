"""
File name: Global.py 
Description: This file contain all the necessary global definition used in the different part of the code
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

#-------------------------------------------------------------------------------
PATH_PIT_SKIN = "data/images/pit.png"
PATH_STORE_SKIN = "data/images/store.png"
PATH_BACKGROUND_SKIN = "data/images/background.png"
PATH_BOARD_SKIN = "data/images/board.png"
BOARD_POSITION = (60, 150)
BOARD_SIZE = (537, 200)
STORE_SIZE = (62, 140)
PIT_SIZE = (63, 63)
PIT_GAP = (2, 13)
BORDER_GAP = (10, 30)
TOP_PIT_Y = BOARD_POSITION[1] + BORDER_GAP[1]
BOT_PIT_Y = BOARD_POSITION[1] + BORDER_GAP[1] + PIT_SIZE[1] + PIT_GAP[1]
FIRST_PIT_X_OFFSET = 0
FIRST_PIT_POS = (BOARD_POSITION[0] + BORDER_GAP[0] + STORE_SIZE[0] + PIT_GAP[0] + FIRST_PIT_X_OFFSET, TOP_PIT_Y)
# Define some colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)


def Debug( *msg ):
	print("[DEBUG]:",*msg)
