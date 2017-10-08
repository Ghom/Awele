"""
File name: Global.py 
Description: This file contain all the necessary global definition used in the different part of the code
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

#-------------------------------------------------------------------------------
# The images path used in the different views
import os
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_PIT_SKIN = BASE_PATH+"/data/images/pit.png"
PATH_STORE_SKIN = BASE_PATH+"/data/images/store.png"
PATH_BACKGROUND_SKIN = BASE_PATH+"/data/images/background.png"
PATH_BOARD_SKIN = BASE_PATH+"/data/images/board.png"
PATH_SEEDS_MATRIX = BASE_PATH+"/data/images/seeds.png"

#--------------------------------------------------------------------------------
# Game view position and size reference
#TODO: replace some of those define using and get them form images dynamically
BOARD_POSITION = (60, 150)
BOARD_SIZE = (537, 200)
STORE_SIZE = (62, 140)
PIT_SIZE = (63, 63)
PIT_GAP = (2, 13)
SEED_TEXT_SIZE = 50 # the texture of a seed is 50x50 px
SEED_SIZE = 30 # scale the seed to a wanted size in px
BORDER_GAP = (10, 30)
TOP_PIT_Y = BOARD_POSITION[1] + BORDER_GAP[1]
BOT_PIT_Y = BOARD_POSITION[1] + BORDER_GAP[1] + PIT_SIZE[1] + PIT_GAP[1]
FIRST_PIT_X_OFFSET = 0
FIRST_PIT_POS = (BOARD_POSITION[0] + BORDER_GAP[0] + STORE_SIZE[0] + PIT_GAP[0] + FIRST_PIT_X_OFFSET, TOP_PIT_Y)

#--------------------------------------------------------------------------------
# Game events global definition
MOUSE_UP = 0
MOUSE_DOWN = 1

#---------------------------------------------------------------------------------
# Define some colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)

#---------------------------------------------------------------------------------
# Game UI type selection
GRAPHIC_UI = 0
CONSOL_UI = 1
# UI_TYPE = CONSOL_UI
UI_TYPE = GRAPHIC_UI

#----------------------------------------------------------------------------------
def Debug( *msg ):
    # print("[DEBUG]:",*msg)
    pass
