import pygame
from pygame.locals import *

from Global import Debug

#TODO: Remove Event suffixe from the events names

""" The Event Manager is the Subject part of the MVC architecture.
The Observers(Views, Models and Controllers) can register themeself in order to receive the stream of broadcasted event.
This file also defines all the event that can be posted by the EventManager.
"""
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
""" Generic Event used to construct all the other Events signal """

class Event:
        def __init__(self):
            self.name = "Generic Event"

#------------------------------------------------------------------------------
""" Controllers related events """

class LeftClickEvent(Event):
        # from mousse controller
        # emmited whenever the user left click on the screen surface
        def __init__(self, pos):
            self.name = "Left Click Event"
            self.pos = pos

class QuitEvent(Event):
        # from mousse controller
        # emitted whe user click default quit button part of window
        def __init__(self):
            self.name = "Quit Event"

class TickEvent(Event):
        # from CPU controller
        # emitted by the main loop as fast as the CPU can manage
        def __init__(self):
            self.name = "CPU Tick Event"

#------------------------------------------------------------------------------
""" Sprites related events """

class PitClickedEvent(Event):
        # from the pit sprite on the game view
        # emmited when user left click on pit
        def __init__(self, pit):
            self.name = "Pit Clicked Event"
            self.pit = pit

class StartButtonClickedEvent(Event):
        # from the start button on the menu view
        # emmited when user left click on button
        def __init__(self):
            self.name = "Start Button Clicked Event"

class MenuButtonClickedEvent(Event):
        # from the menu button on the score view
        # emmited when user left click on button
        def __init__(self):
            self.name = "Menu Button Clicked Event"

#------------------------------------------------------------------------------
""" Views related events """

class StartGameEvent(Event):
        # from menu view
        # emitted when the user click the start button
        def __init__(self):
            self.name = "Start Game Event"
            
class PauseGameEvent(Event):
        # This will come from the game view
        # (not used for now) 
        def __init__(self, game):
            self.name = "Pause Game Event"
            self.game = game

class EndScoreEvent(Event):
        # from score view
        # emitted when the user click the menu button
        def __init__(self):
            self.name = "End Score Event"

#------------------------------------------------------------------------------
""" Game related events """

class SeedDistributionCompleteEvent(Event):
        # from container (pit/store)
        # emitted when the last seed has been distributed
        # container: reference the container where the last seed ended
        def __init__(self, container):
            self.name = "Seed Distribution Complete Event"
            self.container = container

class GameStartedEvent(Event):
        # from the game 
        # emmited when the game has finished to initialise
        # game: reference the the game instance
        def __init__(self, game):
            self.name = "Game Started Event"
            self.game = game

class EndGameEvent(Event):
        # from the game 
        # emmited when the game is finished
        # game: reference the the game instance
        def __init__(self, game):
            self.name = "End Game Event"
            self.game = game
            
class TextInfoEvent(Event):
        # from the game
        # emmited whenever the text info box need to be updated on the game view
        # text: the text to display
        # append: boolean indicating if the text needs to be appended to the previous text (if false the previous text is cleared)
        def __init__(self, text, append=False):
            self.name = "Text info Event"
            self.text = text
            self.append = append
