"""
File name: AI_player.py
Description: This file contain the AI mecanics to play Awele against a human player
The AI use the minimax algorithm to determine the best move to play
Author: Guillaume Paniagua
Creation date: 08/10/2017
"""

from EventManager import *
from Game import *

class AI_player:
    """AI_player class is the entry point of the AI engine
    """ 
    def __init__(self, event_manager, game):
        self.event_manager = event_manager
        self.event_manager.register_listener( self )
        
        # We don't want the game_tester to post event to the global event_manager
        # so we create another one for the AI only
        self.AI_event_manager = EventManager()

        self.game_tester = Game(self.AI_event_manager, game) # copy constructor
        pass
        
    #----------------------------------------------------------------------
    def notify(self, event):
        """notify is the incoming point of events reception
        """ 
        #if isinstance(event, PitClickedEvent ):
        pass