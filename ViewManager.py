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
            self.back_sprites = pygame.sprite.RenderUpdates()
            self.pit_sprites = pygame.sprite.RenderUpdates()
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
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        pit_sprite.rect.x = FIRST_PIT_POS[0] + (5-container.id) * (PIT_GAP[0] + PIT_SIZE[0])
                        pit_sprite.rect.y = FIRST_PIT_POS[1]
                    if isinstance(container, Store):
                        # Add StoreSprite binded with a Store to the render group and place it on the board
                        store_sprite = StoreSprite( container, self.pit_sprites )
                        store_sprite.rect.x = BOARD_POSITION[0] + BORDER_GAP[0]
                        store_sprite.rect.y = BOARD_POSITION[1] + BORDER_GAP[1]

                # player 1 owned the bottom pits and they need to be constructed from LEFT to RIGHT (1 - 6)
                for container in game.player1.pit_list:
                    if isinstance(container, Pit):
                        # Add PitSprite binded with a Pit to the render group and place it on the board
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        pit_sprite.rect.x = FIRST_PIT_POS[0] + container.id * (PIT_GAP[0] + PIT_SIZE[0])
                        pit_sprite.rect.y = FIRST_PIT_POS[1] + PIT_SIZE[1] + PIT_GAP[1]
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

				
#-------------------------------------------------------------------------------
#TODO: create an bastract class Container that would be base class for PitSprite and StoreSprite
# to remove redundancy in code
class PitSprite(pygame.sprite.Sprite):
        """PitSprite is used to create a pit on the screen.
        For now the pit is an invisible clicking zone displaying a number of seeds
        """
        def __init__(self, event_manager, pit, group=()):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            # binding to a specific pit object of the game
            self.pit = pit
            
            pygame.sprite.Sprite.__init__(self, group)
		
            # Draw a rectangular transparent surface
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)
            self.rect = self.image.get_rect()

            # add a number representing the number of seeds of binded pit in the center
            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.pit.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( PIT_SIZE[0]/2, PIT_SIZE[1]/2 ))
        
        #----------------------------------------------------------------------
        def update(self):
            """update draw the graphics element of the pit sprite with potentially new data
            """
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)

            myfont = pygame.font.SysFont("monospace", 15)
            # the data (number of seeds) get updated by poking into the binded pit
            text = str(self.pit.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( PIT_SIZE[0]/2, PIT_SIZE[1]/2 ))
        
        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    # When the user click on the pit surface notify the game
                    self.event_manager.post(PitClickedEvent(self.pit))

#------------------------------------------------------------------------------
class StoreSprite(pygame.sprite.Sprite):
        """StoreSprite is used to create a store on the screen.
        For now the Store is an invisible zone displaying a number of seeds
        """
        def __init__(self, store, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            # binding to a specific store object of the game
            self.store = store

            # Draw a rectangular transparent surface
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)
            self.rect = self.image.get_rect()

            # add a number representing the number of seeds of binded store in the center
            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.store.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( STORE_SIZE[0]/2, STORE_SIZE[1]/2 ))

        def update(self):
            """update draw the graphics element of the store sprite with potentially new data
            """
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)

            myfont = pygame.font.SysFont("monospace", 15)
            # the data (number of seeds) get updated by poking into the binded pit
            text = str(self.store.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( STORE_SIZE[0]/2, STORE_SIZE[1]/2 ))
            
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