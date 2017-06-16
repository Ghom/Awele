"""
File name: EventManager.py 
Description: The Event Manager is the Subject part of the MVC architecture.
The Observers(Views, Models and Controllers) can register themeself in order to receive the stream of broadcasted event.
This file also defines all the event that can be posted by the EventManager.
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

import pygame
from pygame.locals import *

from Global import Debug

#TODO: Remove Event suffixe from the events names

#------------------------------------------------------------------------------
class EventManager:
        """EventManager is responsible for coordinating most communication
        between the Model, View, and Controller. His role is to keep track
        of the different observer and notify them when someone post an event
        """
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
class Event:
        """Event is Generic event used to construct all the other Events signal
        """
        def __init__(self):
            self.name = "Generic Event"

#------------------------------------------------------------------------------
# Controllers related events

class LeftClickEvent(Event):
        """LeftClickEvent is emmited from mousse controller
        whenever the user left click on the screen surface
        """
        def __init__(self, pos):
            self.name = "Left Click Event"
            self.pos = pos

class QuitEvent(Event):
        """QuitEvent is emmited from mousse controller
        when user click default quit button part of window
        """
        def __init__(self):
            self.name = "Quit Event"

class TickEvent(Event):
        """TickEvent is emmited from CPUSpinnerController
        as fast as the CPU can manage, mainly used to refresh
        the views and scan for incoming user events
        """
        def __init__(self):
            self.name = "CPU Tick Event"

#------------------------------------------------------------------------------
# Sprites related events

class PitClickedEvent(Event):
        """PitClickedEvent s emmited from the pit sprites on the game view
        when user left click on a pit sprite
        """
        def __init__(self, pit):
            self.name = "Pit Clicked Event"
            self.pit = pit

class StartButtonClickedEvent(Event):
        """StartButtonClickedEvent is emmited from the start button 
        on the menu view when the user left click on the button
        """
        def __init__(self):
            self.name = "Start Button Clicked Event"

class MenuButtonClickedEvent(Event):
        """MenuButtonClickedEvent is emmited from the menu button
        on the score view when the user left click on button
        """
        def __init__(self):
            self.name = "Menu Button Clicked Event"

#------------------------------------------------------------------------------
# Views related events

class StartGameEvent(Event):
        """StartGameEvent is emmited from the menu view
        when the user left click on the start button
        """
        def __init__(self):
            self.name = "Start Game Event"
            
class PauseGameEvent(Event):
        """(not used for now)PauseGameEvent This will come from the game view
        """
        def __init__(self, game):
            self.name = "Pause Game Event"
            self.game = game

class EndPauseGameEvent(Event):
        """(not used for now)EndPauseGameEvent This will come from the pause view
        """
        def __init__(self, game):
            self.name = "End Pause Game Event"
            self.game = game            

class EndScoreEvent(Event):
        """EndScoreEvent is emitted from the score view
        when the user left click on the menu button
        """
        def __init__(self):
            self.name = "End Score Event"

#------------------------------------------------------------------------------
# Game related events

class SeedDistributionCompleteEvent(Event):
        """SeedDistributionCompleteEvent is emmited from a container, a pit or a store,
        when the last seed has been distributed. This is part of the distribution process
        Attributes:
        container -- reference the container where the last seed ended
        """
        def __init__(self, container):
            self.name = "Seed Distribution Complete Event"
            self.container = container

class GameStartedEvent(Event):
        """GameStartedEvent is emmited from the game 
        when it completed his initialisation
        Attributes:
        game -- reference the the game instance
        """
        def __init__(self, game):
            self.name = "Game Started Event"
            self.game = game

class EndGameEvent(Event):
        """EndGameEvent is emmited from the game 
        when it finish
        Attributes:
        game -- reference the the game instance
        """
        def __init__(self, game):
            self.name = "End Game Event"
            self.game = game
            
class TextInfoEvent(Event):
        """TextInfoEvent is emmited from the game
        whenever the text info box need to be updated on the game view
        Attributes:
        text -- the text to display
        append -- boolean indicating if the text needs to be appended to the previous text, 
        if false the previous text is cleared (default False)
        """
        def __init__(self, text, append=False):
            self.name = "Text info Event"
            self.text = text
            self.append = append
