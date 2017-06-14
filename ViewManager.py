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
        """ViewManager class is starting and stoping the different views according to th incoming events.
        This class also initialising and setting the pygame window.
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
                if isinstance(event, StartGameEvent):
                        # unregister and DELETE the current view if there is any and start the Game view
                        self.purge(self.current_view)
                        self.current_view = BoardView(self.event_manager) # the Game view needs to be started before the game
                        self.game = Game(self.event_manager) # Maybe not the best idea to start the game in the view manager
                        
                if isinstance(event, PauseGameEvent):
                        # unregister but KEEP the current view if there is any and start the Game view
                        self.purge(self.current_view)
                    
                if isinstance(event, EndGameEvent):
                        # unregister and DELETE the current view if there is any and start Score view
                        self.purge(self.current_view)
                        self.current_view = ScoreView(self.event_manager, self.game)
                        
                if isinstance(event, EndScoreEvent):
                        # unregister and DELETE the current view if there is any and start Menu view
                        self.purge(self.game)
                        self.purge(self.current_view)
                        self.current_view = MenuView(self.event_manager) 

#------------------------------------------------------------------------------
class MenuView:
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            
            self.window = pygame.display.get_surface()
            self.back_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)
            self.back_sprites.draw (self.window)
            
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
            self.event_manager.post(StartButtonClickedEvent())
            
        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, TickEvent):
                # refresh page
                self.back_sprites.draw (self.window)
                self.buttons.draw (self.window)
                pygame.display.flip()
                
            if isinstance(event, StartButtonClickedEvent):
                self.event_manager.post(StartGameEvent())
                
#------------------------------------------------------------------------------
#TODO: Rename in GameView
class BoardView:
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            self.window = pygame.display.get_surface()

            self.back_sprites = pygame.sprite.RenderUpdates()
            self.pit_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)

            self.text_info_sprite = TextInfoSprite((BOARD_SIZE[0],30),(BOARD_POSITION[0],80),"",self.back_sprites)

            board = BoardSprite( self.back_sprites )
            board.rect = BOARD_POSITION

            self.back_sprites.draw( self.window )
            pygame.display.flip()

        #----------------------------------------------------------------------
        def init_containers(self, game):

                # player 2 owned the top pits and they need to be constructed from RIGHT to LEFT (1 - 6)
                for container in game.player2.pit_list:
                    if isinstance(container, Pit):
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        pit_sprite.rect.x = FIRST_PIT_POS[0] + (5-container.id) * (PIT_GAP[0] + PIT_SIZE[0])
                        pit_sprite.rect.y = FIRST_PIT_POS[1]
                    if isinstance(container, Store):
                        store_sprite = StoreSprite( container, self.pit_sprites )
                        store_sprite.rect.x = BOARD_POSITION[0] + BORDER_GAP[0]
                        store_sprite.rect.y = BOARD_POSITION[1] + BORDER_GAP[1]

                # player 1 owned the bottom pits and they need to be constructed from LEFT to RIGHT (1 - 6)
                for container in game.player1.pit_list:
                    if isinstance(container, Pit):
                        pit_sprite = PitSprite( self.event_manager, container, self.pit_sprites )
                        pit_sprite.rect.x = FIRST_PIT_POS[0] + container.id * (PIT_GAP[0] + PIT_SIZE[0])
                        pit_sprite.rect.y = FIRST_PIT_POS[1] + PIT_SIZE[1] + PIT_GAP[1]
                    if isinstance(container, Store):
                        store_sprite = StoreSprite( container, self.pit_sprites )
                        store_sprite.rect.x = BOARD_POSITION[0] + BOARD_SIZE[0] - BORDER_GAP[0] - STORE_SIZE[0]
                        store_sprite.rect.y = BOARD_POSITION[1] + BORDER_GAP[1]

                self.pit_sprites.draw( self.window )
                pygame.display.flip()
        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, TickEvent):

                #Draw Everything

                self.background = pygame.Surface( self.window.get_size() )
                self.background.fill( (0,0,0) )
                self.back_sprites.clear( self.window, self.background )
                self.pit_sprites.clear( self.window, self.background )

                self.back_sprites.update()
                self.pit_sprites.update()

                dirtyRects1 = self.back_sprites.draw( self.window )
                dirtyRects2 = self.pit_sprites.draw( self.window )
                
                dirtyRects = dirtyRects1 + dirtyRects2
                pygame.display.update( dirtyRects )
                
            if isinstance(event, GameStartedEvent):
                self.init_containers(event.game)

            if isinstance(event, TextInfoEvent):
                self.text_info_sprite.update(event.text, event.append)

#------------------------------------------------------------------------------
class ScoreView:
        def __init__(self, event_manager, game):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            self.game = game
            
            self.window = pygame.display.get_surface()
            self.window_rect = self.window.get_rect()
            
            self.back_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)
            self.back_sprites.draw (self.window)

            self.text_elements = pygame.sprite.RenderUpdates()
            
            self.title = TextSprite("SCORES", 30, True, self.text_elements)
            self.title.rect.x = self.window_rect.center[0] - self.title.rect.size[0]/2
            self.title.rect.y = 25
            
            text_p1 = self.game.player1.name+" ended with "+ str(self.game.player1.pit_list[6].seeds)+ " seeds"
            self.title = TextSprite(text_p1, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 125

            text_p2 = self.game.player2.name+" ended with "+ str(self.game.player2.pit_list[6].seeds)+ " seeds"
            self.title = TextSprite(text_p2, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 175

            if self.game.winner != None:
                text_winner = self.game.winner.name+" won the game with "+ str(self.game.winner.pit_list[6].seeds)+ " seeds. Congratulation!"
            else:
                text_winner = "This is a draw, well played it was a tight battle"
            self.title = TextSprite(text_winner, 20, True, self.text_elements)
            self.title.rect.x = 10
            self.title.rect.y = 225

            
            self.text_elements.draw (self.window)
            
            self.buttons = pygame.sprite.RenderUpdates()
            text = "MENU"
            size = (200,70)
            color = WHITE
            callback = self.MenuButtonClickedCB
            self.start_button = PushButton(self.event_manager, text, size, color, callback, self.buttons)

            self.start_button.rect.x = self.window_rect.center[0]-size[0]/2
            self.start_button.rect.y = self.window_rect.size[1]-2*size[1]
            self.buttons.draw (self.window)
            
            pygame.display.flip()

        #----------------------------------------------------------------------
        def MenuButtonClickedCB(self):
            self.event_manager.post(MenuButtonClickedEvent())
            
        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, TickEvent):
                # refresh page
                self.back_sprites.draw (self.window)
                self.text_elements.draw (self.window)
                self.buttons.draw (self.window)
                pygame.display.flip()
                
            if isinstance(event, MenuButtonClickedEvent):
                self.event_manager.post(EndScoreEvent())

				
#-------------------------------------------------------------------------------
class PitSprite(pygame.sprite.Sprite):
        def __init__(self, event_manager, pit, group=()):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            self.pit = pit
            
            pygame.sprite.Sprite.__init__(self, group)
            #self.image = pygame.image.load(PATH_PIT_SKIN).convert()
		
            # Draw a rectangle on a transparent white surface
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)
            self.rect = self.image.get_rect()

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.pit.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( PIT_SIZE[0]/2, PIT_SIZE[1]/2 ))

        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    self.event_manager.post(PitClickedEvent(self.pit))

        def update(self):
            #Debug("Update pit sprite of pit",self.pit.id,"containing",self.pit.seeds,"seeds")
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.pit.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( PIT_SIZE[0]/2, PIT_SIZE[1]/2 ))

#------------------------------------------------------------------------------
class StoreSprite(pygame.sprite.Sprite):
        def __init__(self, store, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            #self.image = pygame.image.load(PATH_STORE_SKIN).convert()
            self.store = store

            # Draw a rectangle on a transparent white surface
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)
            self.rect = self.image.get_rect()

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.store.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( STORE_SIZE[0]/2, STORE_SIZE[1]/2 ))

        def update(self):
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            #pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.store.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, ( STORE_SIZE[0]/2, STORE_SIZE[1]/2 ))
            
#------------------------------------------------------------------------------
class BackgroundSprite(pygame.sprite.Sprite):
        def __init__(self, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BACKGROUND_SKIN).convert()
            
#------------------------------------------------------------------------------
class BoardSprite(pygame.sprite.Sprite):
        def __init__(self, group=()):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BOARD_SKIN).convert()

#------------------------------------------------------------------------------
class TextInfoSprite(pygame.sprite.Sprite):
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

            self.myfont = pygame.font.SysFont("monospace", 15)
            label = self.myfont.render(self.text, 1, BLACK)
            self.image.blit(label, ( 10, (self.size[1]/2)-10 ))

        def update(self, text=None, append=False):
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
        def __init__(self, event_manager, text, size, color, callback, group=()):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            self.text = text
            self.size = size
            self.color = color
            self.callback = callback
            
            pygame.sprite.Sprite.__init__(self, group)

            self.image = pygame.Surface(self.size).convert()
            self.image.fill(self.color)
            pygame.draw.rect(self.image, BLACK, [ (0,0), self.size ], 10)
            self.rect = self.image.get_rect()

            font_size = 20 
            self.myfont = pygame.font.SysFont("monospace", font_size, True)
            label = self.myfont.render(self.text, 1, BLACK)
            text_size = len(self.text)
            self.image.blit(label, ( (self.size[0]/2)-(text_size*(font_size+3)/2)/2, (self.size[1]/2)-(font_size/2) ))

        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    self.callback()