import pygame
from pygame.locals import *

def Debug( *msg ):
	print("[DEBUG]:",*msg)

class Event:
        def __init__(self):
            self.name = "Generic Event"

class LeftClickEvent(Event):
        def __init__(self, pos):
            self.name = "Left Click Event"
            self.pos = pos

class PitClickedEvent(Event):
        def __init__(self, pit):
            self.name = "Pit Clicked Event"
            self.pit = pit

class SeedDistributionCompleteEvent(Event):
        def __init__(self, container):
            self.name = "Seed Distribution Complete Event"
            self.container = container

class TickEvent(Event):
        def __init__(self):
            self.name = "CPU Tick Event"

class GameStartedEvent(Event):
        def __init__(self, game):
            self.name = "Game Started Event"
            self.game = game
            
class QuitEvent(Event):
        def __init__(self):
            self.name = "Quit Event"

#------------------------------------------------------------------------------
class EventManager:
	"""this object is responsible for coordinating most communication
	between the Model, View, and Controller."""
	def __init__(self):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()
		self.event_queue= []

	#----------------------------------------------------------------------
	def register_listener( self, listener ):
		self.listeners[ listener ] = 1

	#----------------------------------------------------------------------
	def unregister_listener( self, listener ):
		if listener in self.listeners:
			del self.listeners[ listener ]
		
	#----------------------------------------------------------------------
	def post( self, event ):
		if not isinstance(event, TickEvent):
			Debug( "     Message: " + event.name )
		for listener in list(self.listeners):
			#NOTE: If the weakref has died, it will be 
			#automatically removed, so we don't have 
			#to worry about it.
			listener.notify( event )

#------------------------------------------------------------------------------
class MousseController:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener( self )
        
    #---------------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                        ev = QuitEvent()
                        
                if event.type == MOUSEBUTTONDOWN: 
                    if event.button == 1:
                        ev = LeftClickEvent( event.pos )

                if ev:
                    self.event_manager.post( ev )
                    
#------------------------------------------------------------------------------
class KeyboardController:
        """KeyboardController takes Pygame events generated by the
        keyboard and uses them to control the model, by sending Requests
        or to control the Pygame display directly, as with the QuitEvent
        """
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

    #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance( event, TickEvent ):
                #Handle Input Events
                return

#------------------------------------------------------------------------------ 
class CPUSpinnerController:
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            self.clock = pygame.time.Clock()    
            self.keep_going = True
            
        #----------------------------------------------------------------------
        def run(self):
            while self.keep_going:
                self.clock.tick(30)
                event = TickEvent()
                self.event_manager.post(event)
            pygame.quit()

        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, QuitEvent):
                self.keep_going = False


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

#-------------------------------------------------------------------------------
class PitSprite(pygame.sprite.Sprite):
        def __init__(self, event_manager, pit, group=None):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )
            self.pit = pit
            
            pygame.sprite.Sprite.__init__(self, group)
            #self.image = pygame.image.load(PATH_PIT_SKIN).convert()
		
            # Draw a rectangle on a transparent white surface
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)
            self.rect = self.image.get_rect()

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.pit.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, self.rect.center)

        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, LeftClickEvent):
                if self.rect.collidepoint(event.pos):
                    self.event_manager.post(PitClickedEvent(self.pit))

        def update(self):
            #Debug("Update pit sprite of pit",self.pit.id,"containing",self.pit.seeds,"seeds")
            self.image = pygame.Surface(PIT_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, RED, [ (0,0), PIT_SIZE ], 1)

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.pit.seeds)
            self.image = label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, self.rect.center)

#------------------------------------------------------------------------------
class StoreSprite(pygame.sprite.Sprite):
        def __init__(self, store, group=None):
            pygame.sprite.Sprite.__init__(self, group)
            #self.image = pygame.image.load(PATH_STORE_SKIN).convert()
            self.store = store

            # Draw a rectangle on a transparent white surface
            self.image = pygame.Surface(STORE_SIZE).convert_alpha()
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, RED, [ (0,0), STORE_SIZE ], 1)
            self.rect = self.image.get_rect()

            myfont = pygame.font.SysFont("monospace", 15)
            text = str(self.store.seeds)
            label = myfont.render(text, 1, YELLOW)
            self.image.blit(label, self.rect.center)
            
#------------------------------------------------------------------------------
class BackgroundSprite(pygame.sprite.Sprite):
        def __init__(self, group=None):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BACKGROUND_SKIN).convert()
            
#------------------------------------------------------------------------------
class BoardSprite(pygame.sprite.Sprite):
        def __init__(self, group=None):
            pygame.sprite.Sprite.__init__(self, group)
            self.image = pygame.image.load(PATH_BOARD_SKIN).convert()
            
#------------------------------------------------------------------------------
class BoardView:
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            pygame.init()
            #open a 640x480 window
            self.window = pygame.display.set_mode((640, 480))
            pygame.display.set_caption( 'Awele' )
            font = pygame.font.Font(None, 30)

            self.back_sprites = pygame.sprite.RenderUpdates()
            self.pit_sprites = pygame.sprite.RenderUpdates()
            background = BackgroundSprite( self.back_sprites )
            background.rect = (0, 0)

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
        
#------------------------------------------------------------------------------
class Container:
        """ Abstract class that represent board container such as Pits and Stores """
        def __init__(self):
            self.event_manager = None
            self.next = None
            self.seeds = 0

        #----------------------------------------------------------------------
        def pass_seeds(self, seeds):
            self.seeds += 1
            seeds -= 1
            if isinstance(self, Pit):
                Debug("Pit",self.id,"now contain",self.seeds,"seeds")
            else:
                Debug("Store now contain",self.seeds,"seeds")
            if seeds > 0:
                self.next.pass_seeds(seeds)
            else:
                self.event_manager.post(SeedDistributionCompleteEvent(self))

        #----------------------------------------------------------------------
        def add_seed(self, amount):
            self.seeds += amount
            return self.seeds 

        #----------------------------------------------------------------------
        def remove_seed(self, amount):
            self.seeds -= amount
            return self.seeds

        #----------------------------------------------------------------------
        def take_seeds(self):
            amount = self.seeds
            self.seeds = 0
            return amount
            
#------------------------------------------------------------------------------
class Pit(Container):
        def __init__(self, event_manager, id_nb, next_container):
            Container.__init__(self)
            self.event_manager = event_manager
            
            self.id = id_nb
            self.next = next_container
            self.seeds = 6

        def distribute(self):
            seeds = self.seeds
            self.seeds = 0
            Debug("Distribute",seeds,"from pit",self.id)
            Debug("Pit",self.id,"now contain",self.seeds,"seeds")
            self.next.pass_seeds(seeds)
                        
#------------------------------------------------------------------------------
class Store(Container):
        def __init__(self, event_manager, next_container):
            Container.__init__(self)
            self.event_manager = event_manager
            # No need to register as a listener because we are only posting event from Store object
            #self.event_manager.register_listener( self )

            self.next = next_container

#------------------------------------------------------------------------------
class Player:
        def __init__(self, name, pit_list=None):
            self.name = name
            self.score = 0
            self.pit_list = pit_list

#------------------------------------------------------------------------------
class Game:
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            # Construct a list in reverse order the list containing [pit1 ... pit6, store] for both player
            # The construction is made in reverse order to allow to give the field next for the newly created pit
            store_p1 = Store(self.event_manager, None)
            store_p2 = Store(self.event_manager, None)
            p1_pits = [store_p1]
            p2_pits = [store_p2]
            next_p1 = store_p1
            next_p2 = store_p2
            for i in range(6,0,-1):
                next_p1 = pit_p1 = Pit(self.event_manager, i-1, next_p1)
                next_p2 = pit_p2 = Pit(self.event_manager, i-1, next_p2)
                p1_pits.insert(0, pit_p1)
                p2_pits.insert(0, pit_p2)
            # Finally fill the next field for the Stores created at the begining
            # so the store of each player points toward the first pit of the opposite player
            # and the loop is then closed
            store_p1.next = p2_pits[0]
            store_p2.next = p1_pits[0]

            # Create players and assign them a pit list
            self.player1 = Player("Player 1", p1_pits)
            self.player2 = Player("Player 2", p2_pits)
            self.active_player = self.player1
            self.inactive_player = self.player2

            self.play_again = False

            self.event_manager.post(GameStartedEvent(self))

        #----------------------------------------------------------------------
        def end_turn(self):
            if self.play_again == False:
                self.active_player, self.inactive_player = self.inactive_player, self.active_player
            else:
                self.play_again = False
            Debug("Active player:",self.active_player.name)
        
        #---------------------------------------------------------------------
        def check_special_actions(self, last_pit):
            pit_list_active = self.active_player.pit_list
            pit_list_inactive = self.inactive_player.pit_list
            
            if last_pit in pit_list_active:
                if isinstance(last_pit, Store):
                    # each player only have one Store
                    Debug("SPECIAL: Player last seed ended in his own Store he can play again")
                    self.play_again = True
                elif last_pit.seeds == 1:
                    # means that the last seed ended in an empty pit of his own
                    Debug("SPECIAL: Player last seed ended in an empty pit of his own he can put the content of the opposite pit plus de last seed in his Store")
                    opposite_pit = pit_list_inactive[5 - pit_list_active.id]
                    
                    collected_seeds = opposite_pit.take_seeds() + last_pit.take_seeds()
                    store = pit_list_active[len(pit_list_active)-1]
                    store.add_seed(collected_seeds)

        #----------------------------------------------------------------------
        def notify(self, event):
            if isinstance(event, PitClickedEvent ):
                if event.pit in self.active_player.pit_list:
                    event.pit.distribute()
                else:
                    Debug("This pit doesn't belong to you")
            if isinstance(event, SeedDistributionCompleteEvent ):
                self.check_special_actions(event.container)
                self.end_turn()
#------------------------------------------------------------------------------
def main():
        """..."""
        event_manager = EventManager()

        board_view = BoardView( event_manager )

        # No keyboard needed for now
        #keybd = KeyboardController( event_manager )
        mousse = MousseController ( event_manager ) 
        spinner = CPUSpinnerController( event_manager )

        game = Game(event_manager)

        spinner.run()

if __name__ == "__main__":
        main()
