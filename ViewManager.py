"""
File name: ViewManager.py 
Description: This file contains the different view of the game and a class that switch from one to another (ViewManager)
This file also contains the sprites definition used to construct the different views.
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

import pygame
from pygame.locals import *

from EventManager import *
from Game import *

from Global import *

#------------------------------------------------------------------------------
class ViewManager:
        """ViewManager class is starting and stoping the different views according to the incoming events.
        This class also initialising and set the pygame window.
        """
        def __init__(self, event_manager):
                self.event_manager = event_manager
                self.event_manager.register_listener(self)

                pygame.init()
                #open a 640x480 window
                self.window = pygame.display.set_mode((640, 480))
                pygame.display.set_caption( 'Awele' )
                font = pygame.font.Font(None, 30)
                
                self.current_view = MenuView(self.event_manager)
                
        #----------------------------------------------------------------------
        def purge(self, object):
                """Purge method unregister the object from the EventManager and delete it"""
                self.event_manager.unregister_listener(object)
                del object
                
        #----------------------------------------------------------------------
        def notify(self, event):
                """notify is the incoming point of events reception
                """
                if isinstance(event, StartGameEvent):
                        # Purge the menu view and start the game view
                        self.purge(self.current_view)
                        self.current_view = GameView(self.event_manager) # the Game view needs to be started before the game
                        self.game = Game(self.event_manager) # Maybe not the best idea to start the game in the view manager
                        
                if isinstance(event, PauseGameEvent):
                        # Purge the game view and start the pause view
                        self.purge(self.current_view)
                        
                if isinstance(event, EndPauseGameEvent):
                        # Purge the pause view and start the game view
                        self.purge(self.current_view)
                        
                if isinstance(event, EndGameEvent):
                        # Purge the game view and start the score view
                        self.purge(self.current_view)
                        self.current_view = ScoreView(self.event_manager, self.game)
                        
                if isinstance(event, EndScoreEvent):
                        # Purge the score view and start the menu view
                        self.purge(self.game)
                        self.purge(self.current_view)
                        self.current_view = MenuView(self.event_manager) 

#------------------------------------------------------------------------------
class MenuView:
        """MenuView holds all the graphics component of the menu and draw them on CPU tick
        """
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            
            # Get the window surface and draw background
            self.window = pygame.display.get_surface()
            self.back_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)
            self.back_sprites.draw (self.window)
            
            # Create a START push button and draw it
            self.buttons = pygame.sprite.RenderUpdates()
            text = "START"
            size = (200,70)
            color = WHITE
            callback = self.StartButtonClickedCB
            self.start_button = PushButton(self.event_manager, text, size, color, callback, self.buttons)
            center = self.window.get_rect().center
            x = center[0]-size[0]/2
            y = center[1]-size[1]/2
            self.start_button.rect.x = x
            self.start_button.rect.y = y
            self.buttons.draw (self.window)
            
            pygame.display.flip()

        #----------------------------------------------------------------------
        def StartButtonClickedCB(self):
            """ This is the call back that is registered to the Start button on 
            the menu view. It get called when the user click on the Start button.
            """
            self.event_manager.post(StartButtonClickedEvent())
            
        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, TickEvent):
                # refresh page
                self.back_sprites.draw (self.window)
                self.buttons.draw (self.window)
                pygame.display.flip()
                
            if isinstance(event, StartButtonClickedEvent):
                self.event_manager.post(StartGameEvent())
                
#------------------------------------------------------------------------------
class GameView:
        """GameView holds all the graphics components of the game view and draw them on CPU tick
        """
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            
            # get the window surface
            self.window = pygame.display.get_surface()
    
            # add background
            self.back_sprites = pygame.sprite.LayeredUpdates()
            self.pit_sprites = pygame.sprite.LayeredUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)

            # add a text box
            self.text_info_sprite = TextInfoSprite((BOARD_SIZE[0],30),(BOARD_POSITION[0],80),"",self.back_sprites)

            # add the board
            board = BoardSprite( self.back_sprites )
            board.rect = BOARD_POSITION

            # draw everything on the window surface
            self.back_sprites.draw( self.window )
            pygame.display.flip()

        #----------------------------------------------------------------------
        def init_containers(self, game):
                """init_containers method will create all the necessary sprite to hold the pits and stores state
                """
                # player 2 owned the top pits and they need to be constructed from RIGHT to LEFT (1 - 6)
                for container in game.player2.pit_list:
                    if isinstance(container, Pit):
                        # Add PitSprite binded with a Pit to the render group and place it on the board
                        # pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        # pit_sprite.rect.x = FIRST_PIT_POS[0] + (5-container.id) * (PIT_GAP[0] + PIT_SIZE[0])
                        # pit_sprite.rect.y = FIRST_PIT_POS[1]
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        x = FIRST_PIT_POS[0] + (5-container.id) * (PIT_GAP[0] + PIT_SIZE[0])
                        y = FIRST_PIT_POS[1]
                        pit_sprite.update_pos(x, y)
                        self.pit_sprites.change_layer(pit_sprite, 1)
                    if isinstance(container, Store):
                        # Add StoreSprite binded with a Store to the render group and place it on the board
                        store_sprite = StoreSprite( container, self.pit_sprites )
                        store_sprite.rect.x = BOARD_POSITION[0] + BORDER_GAP[0]
                        store_sprite.rect.y = BOARD_POSITION[1] + BORDER_GAP[1]

                # player 1 owned the bottom pits and they need to be constructed from LEFT to RIGHT (1 - 6)
                for container in game.player1.pit_list:
                    if isinstance(container, Pit):
                        # Add PitSprite binded with a Pit to the render group and place it on the board
                        # pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        # pit_sprite.rect.x = FIRST_PIT_POS[0] + container.id * (PIT_GAP[0] + PIT_SIZE[0])
                        # pit_sprite.rect.y = FIRST_PIT_POS[1] + PIT_SIZE[1] + PIT_GAP[1]
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        x = FIRST_PIT_POS[0] + container.id * (PIT_GAP[0] + PIT_SIZE[0])
                        y = FIRST_PIT_POS[1] + PIT_SIZE[1] + PIT_GAP[1]
                        pit_sprite.update_pos(x, y)
                        self.pit_sprites.change_layer(pit_sprite, 1)
                    if isinstance(container, Store):
                        # Add StoreSprite binded with a Store to the render group and place it on the board
                        store_sprite = StoreSprite( container, self.pit_sprites )
                        store_sprite.rect.x = BOARD_POSITION[0] + BOARD_SIZE[0] - BORDER_GAP[0] - STORE_SIZE[0]
                        store_sprite.rect.y = BOARD_POSITION[1] + BORDER_GAP[1]

                # draw the render group containing all the pit and store sprites
                self.pit_sprites.draw( self.window )
                pygame.display.flip()
        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, TickEvent):
                #Draw Everything on tick event

                self.background = pygame.Surface( self.window.get_size() )
                self.background.fill( (0,0,0) )
                self.back_sprites.clear( self.window, self.background )
                self.pit_sprites.clear( self.window, self.background )
                
                self.back_sprites.update()
                self.pit_sprites.update()

                dirtyRects1 = self.back_sprites.draw( self.window )
                dirtyRects2 = self.pit_sprites.draw( self.window )

                # Using the dirty rectangle method to draw the game avoid updating the entire screen
                # it only update the differences
                dirtyRects = dirtyRects1 + dirtyRects2
                pygame.display.update( dirtyRects )
                
            if isinstance(event, GameStartedEvent):
                # when the game start create the containers with their seeds 
                self.init_containers(event.game)

            if isinstance(event, TextInfoEvent):
                # update the text in the text box
                self.text_info_sprite.update(event.text, event.append)

#------------------------------------------------------------------------------
class ScoreView:
        """ScoreView holds all the graphics components of the score view and draw them on CPU tick
        """
        def __init__(self, event_manager, game):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            self.game = game
            
            # get window surface and store it size 
            self.window = pygame.display.get_surface()
            self.window_rect = self.window.get_rect()
            
            # draw the background
            self.back_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)
            self.back_sprites.draw (self.window)

            self.text_elements = pygame.sprite.RenderUpdates()
            # add text element to display the window title
            self.title = TextSprite("SCORES", 30, True, self.text_elements)
            self.title.rect.x = self.window_rect.center[0] - self.title.rect.size[0]/2
            self.title.rect.y = 25
            
            # add text element for the player 1 score
            text_p1 = self.game.player1.name+" ended with "+ str(self.game.player1.pit_list[6].seeds)+ " seeds"
            self.title = TextSprite(text_p1, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 125
            
            # add text element for the player 2 score
            text_p2 = self.game.player2.name+" ended with "+ str(self.game.player2.pit_list[6].seeds)+ " seeds"
            self.title = TextSprite(text_p2, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 175

            # add text element for the winner
            if self.game.winner != None:
                text_winner = self.game.winner.name+" won the game with "+ str(self.game.winner.pit_list[6].seeds)+ " seeds. Congratulation!"
            else:
                text_winner = "This is a draw, well played it was a tight battle"
            self.title = TextSprite(text_winner, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 225

            # draw all the text elements
            self.text_elements.draw (self.window)
            
            # add a menu button to go back to menu screen
            self.buttons = pygame.sprite.RenderUpdates()
            text = "MENU"
            size = (200,70)
            color = WHITE
            callback = self.MenuButtonClickedCB
            self.start_button = PushButton(self.event_manager, text, size, color, callback, self.buttons)

            # place and draw the button
            self.start_button.rect.x = self.window_rect.center[0]-size[0]/2
            self.start_button.rect.y = self.window_rect.size[1]-2*size[1]
            self.buttons.draw (self.window)
            
            pygame.display.flip()

        #----------------------------------------------------------------------
        def MenuButtonClickedCB(self):
            """MenuButtonClickedCB is the callback that is executed when 
            the user click on the menu push button.
            """
            self.event_manager.post(MenuButtonClickedEvent())
            
        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, TickEvent):
                # refresh page
                self.back_sprites.draw (self.window)
                self.text_elements.draw (self.window)
                self.buttons.draw (self.window)
                pygame.display.flip()
                
            if isinstance(event, MenuButtonClickedEvent):
                # when the user click the menu button inform the ViewManager to change the view
                self.event_manager.post(EndScoreEvent())

#------------------------------------------------------------------------------
class AbstractContainerSprite(pygame.sprite.Sprite):
        """AbstractContainerSprite is the base class to create pit and store sprites
        """
        def __init__(self, container, group=()):
            self.group = group
            pygame.sprite.Sprite.__init__(self, group)
            # binding to a specific container object of the game
            self.container = container
            # the list containing the seed sprites in the current container
            self.seed_sprites = []
            # a random angle that will be applied on the seeds to display 
            self.random_angle = random.randint(0, 360)
            self.show_seed_nb = False
            
            self.myfont = pygame.font.SysFont("monospace", 15)
            self.update()
            self.rect = self.image.get_rect()

        
        def add_seeds(self, quantity):
            total_seed = quantity + len(self.seed_sprites)
            self.remove_seeds(len(self.seed_sprites))
            for i in range(total_seed):
                seed = SeedSprite(self.group)
                seed.set_position(len(self.seed_sprites), total_seed, self.random_angle)
                if hasattr(self, 'rect'):
                    seed.update_pos(self.rect.x, self.rect.y)
                self.seed_sprites.append(seed)
                
        def remove_seeds(self, quantity):
            for i in range(quantity):
                seed = self.seed_sprites.pop()
                seed.kill()
        
        def draw_seeds(self):
            diff = self.container.seeds - len(self.seed_sprites)
            
            if(diff > 0):
                self.add_seeds(diff)
            elif(diff < 0):
                self.remove_seeds(abs(diff))
                
        def update_pos(self, x, y):
            self.rect.x = x
            self.rect.y = y
            for seed in self.seed_sprites:
                seed.update_pos(x, y)
            
#-------------------------------------------------------------------------------
class PitSprite(AbstractContainerSprite):
        """PitSprite is used to create a pit on the screen.
        For now the pit is an invisible clicking zone displaying a number of seeds
        """
        def __init__(self, event_manager, pit, group=()):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            AbstractContainerSprite.__init__(self, pit, group)
        
        #----------------------------------------------------------------------
        def update(self):
            """update draw the graphics element of the pit sprite with potentially new data
            """
            # Draw a rectangular transparent surface
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            
            # DEBUG: this show the clicking area in red
            #pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)
            
            self.draw_seeds()
            
            if(self.show_seed_nb):
                # the data (number of seeds) get updated by poking into the binded pit
                text = str(self.container.seeds)
                label = self.myfont.render(text, 1, YELLOW)
                self.image.blit(label, ( PIT_SIZE[0]/2, PIT_SIZE[1]/2 ))

        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    # When the user click on the pit surface notify the game
                    self.event_manager.post(PitClickedEvent(self.container))
            
            if isinstance(event, RightClickEvent):
                if self.rect.collidepoint(event.pos):
                    if(event.action == MOUSE_DOWN):
                        self.show_seed_nb = True
                    elif(event.action == MOUSE_UP):
                        self.show_seed_nb = False
#------------------------------------------------------------------------------
class StoreSprite(AbstractContainerSprite):
        """StoreSprite is used to create a store on the screen.
        For now the Store is an invisible zone displaying a number of seeds
        """
        def __init__(self, store, group=()):
            AbstractContainerSprite.__init__(self, store, group)

        def update(self):
            """update draw the graphics element of the store sprite with potentially new data
            """

            # Draw a rectangular transparent surface
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)

            # the data (number of seeds) get updated by poking into the binded pit
            text = str(self.container.seeds)
            label = self.myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( STORE_SIZE[0]/2, STORE_SIZE[1]/2 ))
            
            self.draw_seeds()

#------------------------------------------------------------------------------
import random
import math
pi = math.pi
class SeedSprite(pygame.sprite.Sprite):
        """SeedSprite holds the graphics to create the seeds 
        """
        def __init__(self, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            # get a random image of a seeds based on a matrix image containing 9 seeds of (size SEED_TEXT_SIZE x SEED_TEXT_SIZE)
            self.random_seed = random.randint(0, 8)
            self.x_pos = 0
            self.y_pos = 0

            # create a surface from the seed texture of the randomly selected seed image [0-8]
            seeds_image = pygame.image.load(PATH_SEEDS_MATRIX).convert()
            self.surface = pygame.Surface((SEED_TEXT_SIZE, SEED_TEXT_SIZE)).convert()
            self.surface.set_colorkey((255,255,255,0))
            self.surface.blit( seeds_image, (0,0), (SEED_TEXT_SIZE* self.random_seed, 0, SEED_TEXT_SIZE, SEED_TEXT_SIZE) )

            # scale the surface to a more appropriate size and display
            self.surface = pygame.transform.scale(self.surface, (SEED_SIZE, SEED_SIZE))
            self.image = self.surface
            self.rect = self.image.get_rect()
        
        def update_pos(self, x, y):
            """update_pos move the seed to a new position
            """
            self.rect.x = x + self.x_pos
            self.rect.y = y + self.y_pos
            
        def set_position(self, pos_id, total_seeds, random_angle):
            """set_position determine and set the position of the seed in the pit
            according to the number of seed present in the pit and the seed number (ordered in a list) 
            NOTE: This function is a hack avoiding creating physics to place the seeds
            """
            # print("total_seed:"+str(total_seeds)+", pos_id:"+str(pos_id)) 
            if(total_seeds == 1):
                # if there is only one seed place it in the center of the pit
                self.x_pos = PIT_SIZE[0]/2 - SEED_SIZE/2
                self.y_pos = PIT_SIZE[1]/2 - SEED_SIZE/2
            elif(pos_id <= 4):
                # for the seeds number 2 to 4 place them at an angle equal to 
                # 360°/(seed number). If there is more seed than 4 in the pit
                # that angle is always 90°
                angle = (360/(total_seeds if total_seeds < 4 else 4))
                angle_rad = (((pos_id-1)*pi*angle)+(pi*random_angle))/180
                rot_x = math.cos(angle_rad)
                rot_y = math.sin(angle_rad)
                self.x_pos = rot_x*0.7 * PIT_SIZE[0]/4 + PIT_SIZE[0]/2 - SEED_SIZE/2
                self.y_pos = rot_y*0.7 * PIT_SIZE[1]/4 + PIT_SIZE[1]/2 - SEED_SIZE/2
            elif(pos_id <= 8):
                # the following seeds in between 5 and 8 are place at an angle of 90°
                # a bit further away from the center of the pit
                angle = 90*(pos_id - 8)  + 45
                angle_rad = ((pi*angle)+(pi*random_angle))/180
                rot_x = math.cos(angle_rad)
                rot_y = math.sin(angle_rad)
                self.x_pos = rot_x*1.15 * PIT_SIZE[0]/4 + PIT_SIZE[0]/2 - SEED_SIZE/2
                self.y_pos = rot_y*1.15 * PIT_SIZE[1]/4 + PIT_SIZE[1]/2 - SEED_SIZE/2
            else:
                # from the 9th seed averything is placed randomly within the pit
                self.x_pos = random.uniform(-1.0, 1.0) * PIT_SIZE[0]/4 + PIT_SIZE[0]/2 - SEED_SIZE/2
                self.y_pos = random.uniform(-1.0, 1.0) * PIT_SIZE[1]/4 + PIT_SIZE[1]/2 - SEED_SIZE/2
            
#------------------------------------------------------------------------------
class BackgroundSprite(pygame.sprite.Sprite):
        """BackgroundSprite holds the graphics to create the background 
        """
        def __init__(self, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BACKGROUND_SKIN).convert()
            
#------------------------------------------------------------------------------
class BoardSprite(pygame.sprite.Sprite):
        """BoardSprite holds the graphics to create the board 
        """
        def __init__(self, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BOARD_SKIN).convert()

#------------------------------------------------------------------------------
class TextInfoSprite(pygame.sprite.Sprite):
        """TextInfoSprite is a graphic object that is used to create text box
        that can be updated to print different info messages.
        """
        def __init__(self, size, position, text, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.size = size
            self.text = text
            self.position = position
            
            # Draw a white rectangle surrounded by black border
            self.image = pygame.Surface(self.size).convert()
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, BLACK, [ (0,0), self.size ], 5)
            self.rect = self.image.get_rect()
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

            # insert the text in it
            self.myfont = pygame.font.SysFont("monospace", 15)
            label = self.myfont.render(self.text, 1, BLACK)
            self.image.blit(label, ( 10, (self.size[1]/2)-10 ))

        def update(self, text=None, append=False):
            """update draw the graphic elements of text box with potentially new text
            Note: the previous text can be appended with the new one or completely discarded
            Arguments:
            text -- the text to print (default: None)
            append -- flag if the new text need to be added after the old one or not (default: False)
            """
            if text != None:
                new_text = text
            else:
                new_text = self.text

            if append:
                self.text += new_text
            else:
                self.text = new_text
                
            self.image = pygame.Surface(self.size).convert()
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, BLACK, [ (0,0), self.size ], 5)

            label = self.myfont.render(self.text, 1, BLACK)
            self.image.blit(label, ( 10, (self.size[1]/2)-10 ))

#------------------------------------------------------------------------------
class TextSprite(pygame.sprite.Sprite):
        """TextSprite hold the graphic components to build a text label.
        The text can't be changed once displayed.
        """
        def __init__(self, text, font_size=15, bold=False, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.text = text
            self.font_size = font_size
            self.size = (len(text)*(font_size/2+3), font_size)
            self.bold = bold
            
            # Draw a transparent rectangle area
            self.image = pygame.Surface(self.size).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), self.size ], 1) #Debug surface
            self.rect = self.image.get_rect()

            self.myfont = pygame.font.SysFont("monospace", font_size, self.bold)
            label = self.myfont.render(self.text, 1, BLACK)
            self.image.blit(label, (0,0))

#-------------------------------------------------------------------------------
class PushButton(pygame.sprite.Sprite):
        """PushButton class hold the graphics to draw a button on the screen.
        A callback can be registered to it and called when the button is pressed.
        """
        def __init__(self, event_manager, text, size, color, callback, group=()):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            self.text = text
            self.size = size
            self.color = color
            self.callback = callback
            
            pygame.sprite.Sprite.__init__(self, group)

            #Draw a rectangle of the chosen color surrounded by black borders
            self.image = pygame.Surface(self.size).convert()
            self.image.fill(self.color)
            pygame.draw.rect(self.image, BLACK, [ (0,0), self.size ], 10)
            self.rect = self.image.get_rect()

            # Print the chosen text in the middle of the button
            font_size = 20 
            self.myfont = pygame.font.SysFont("monospace", font_size, True)
            label = self.myfont.render(self.text, 1, BLACK)
            text_size = len(self.text)
            self.image.blit(label, ( (self.size[0]/2)-(text_size*(font_size+3)/2)/2, (self.size[1]/2)-(font_size/2) ))

        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    # call the registered callback when the button is clicked
                    self.callback()