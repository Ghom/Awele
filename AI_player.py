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
        self.AI_event_manager = EventManager("AI")
        print(self.AI_event_manager.listeners.keyrefs())
        
        # keep a copy to the real game to get the new board states
        self.game = game
        self.game_tester = Game(self.AI_event_manager, game) # copy constructor
    
    #----------------------------------------------------------------------
    def play(self):
        self.game_tester.import_board(self.game.export_board())
        tree = []
        self.construct_tree(tree, 3)
        for item in tree:
            print("Recursion:{} Pit:{} Next Player:{} P1_pits:{} P2_pits:{}".format(item[0], item[1]+1, item[2][0].name, item[2][1], item[2][2]))
        
    #----------------------------------------------------------------------
    def construct_tree(self, tree, recursion_depth):
        game_state = self.game_tester.export_board()
        active_player = game_state[0]
        
        for i, val in enumerate(game_state[1 if active_player == self.game_tester.player1 else 2][0:6]):
            self.game_tester.import_board(game_state)
            if(val != 0):
                active_player.pit_list[i].distribute()
                new_state = self.game_tester.export_board()
                tree.append((recursion_depth, i, new_state))
                if(recursion_depth > 0):
                    self.construct_tree(tree, recursion_depth-1)
    
    #----------------------------------------------------------------------
    def notify(self, event):
        """notify is the incoming point of events reception
        """ 
        #if isinstance(event, PitClickedEvent ):
        pass
        
       
class Node:
    self.type = 