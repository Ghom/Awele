import pygame
from pygame.locals import *

from Global import Debug

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

class StartButtonClickedEvent(Event):
        def __init__(self):
            self.name = "Start Button Clicked Event"

class MenuButtonClickedEvent(Event):
        def __init__(self):
            self.name = "Menu Button Clicked Event"
            
class SeedDistributionCompleteEvent(Event):
        def __init__(self, container):
            self.name = "Seed Distribution Complete Event"
            self.container = container

class TickEvent(Event):
        def __init__(self):
            self.name = "CPU Tick Event"

class StartGameEvent(Event):
        def __init__(self):
            self.name = "Start Game Event"

class GameStartedEvent(Event):
        def __init__(self, game):
            self.name = "Game Started Event"
            self.game = game
            
class PauseGameEvent(Event):
        def __init__(self, game):
            self.name = "Pause Game Event"
            self.game = game

class EndScoreEvent(Event):
        def __init__(self):
            self.name = "End Score Event"
   
class EndGameEvent(Event):
        def __init__(self, game):
            self.name = "End Game Event"
            self.game = game
            
class QuitEvent(Event):
        def __init__(self):
            self.name = "Quit Event"

class TextInfoEvent(Event):
        def __init__(self, text, append=False):
            self.name = "Text info Event"
            self.text = text
            self.append = append

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
