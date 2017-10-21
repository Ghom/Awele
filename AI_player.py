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
        node = Node(NodeType.max, 0, self.game_tester.export_board(), root=True)
        move = self.minimax(node, self.game_tester, 3)
        print("Minimax decided to pick pit N°{}".format(move+1))
        self.event_manager.post(PitClickedEvent(self.game.active_player.pit_list[move]))
        # for item in tree:
            # print("Recursion:{} Pit:{} Next Player:{} P1_pits:{} P2_pits:{}".format(item[0], item[1]+1, item[2][0].name, item[2][1], item[2][2]))
        
    #----------------------------------------------------------------------
    def minimax(self, node, game, recursion_depth):
        moves = game.available_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            next_game = game.next_state(move)
            
            # The following trick define the fact that a max_play can call another max_play
            # if the resulting game allow the max player to play again
            
            # If the resulting game belong to "max" aka the computer aka player 2
            if(next_game.active_player == next_game.player2):
                node_type = NodeType.max
                minimax_fct = self.max_play
            # If the resulting game belong to "min" aka the player aka player 1
            elif(next_game.active_player == next_game.player1):
                node_type = NodeType.min
                minimax_fct = self.min_play
                
            child = Node(node_type, move, next_game.export_board())
            node.add_child(child)
            
            if(recursion_depth > 0):
                score = minimax_fct(child, next_game, recursion_depth-1)
            else:
                score = self.evaluate(next_game)
                
            if(score > best_score):
                best_move = move
                best_score = score
        
        return best_move
    
    def min_play(self, node, game, recursion_depth):
        if(game.is_over() or recursion_depth <= 0):
            node.leaf = True
            return self.evaluate(game)
        
        moves = game.available_moves()
        lowest_score = float('inf')
        for move in moves:
            next_game = game.next_state(move)
            
            # The following trick define the fact that a min_play can call another min_play
            # if the resulting game allow the min player to play again
            
            # If the resulting game belong to "max" aka the computer aka player 2
            if(next_game.active_player == next_game.player2):
                node_type = NodeType.max
                minimax_fct = self.max_play
            # If the resulting game belong to "min" aka the player aka player 1
            elif(next_game.active_player == next_game.player1):
                node_type = NodeType.min
                minimax_fct = self.min_play
                
            child = Node(node_type, move, next_game.export_board())
            node.add_child(child)
            
            score = minimax_fct(child, next_game, recursion_depth-1)    
            if(score < lowest_score):
                lowest_score = score
        
        return lowest_score
        
    
    def max_play(self, node, game, recursion_depth):
        if(game.is_over() or recursion_depth <= 0):
            node.leaf = True
            return self.evaluate(game)
        
        moves = game.available_moves()
        best_score = float('-inf')
        for move in moves:
            next_game = game.next_state(move)
            
            # The following trick define the fact that a max_play can call another max_play
            # if the resulting game allow the max player to play again
            
            # If the resulting game belong to "max" aka the computer aka player 2
            if(next_game.active_player == next_game.player2):
                node_type = NodeType.max
                minimax_fct = self.max_play
            # If the resulting game belong to "min" aka the player aka player 1
            elif(next_game.active_player == next_game.player1):
                node_type = NodeType.min
                minimax_fct = self.min_play
                
            child = Node(node_type, move, next_game.export_board())
            node.add_child(child)
            
            score = minimax_fct(child, next_game, recursion_depth-1)    
            if(score > best_score):
                best_score = score
        
        return best_score
    
    def evaluate(self, game):
        # we assume that the computer is always player 2
        game_state = game.export_board()
        # return the difference of scores (player 2 - player 1)
        return game_state[1][6] - game_state[0][6]
    
    #----------------------------------------------------------------------
    def notify(self, event):
        """notify is the incoming point of events reception
        """ 
        #if isinstance(event, PitClickedEvent ):
        pass
        
from enum import Enum
class NodeType(Enum):
    min = 0
    max = 1
    undefined = 2

class Node:
    def __init__(self, node_type, move, game_state, root=False, leaf=False):
        self.type = node_type # min or max node
        self.leaf = leaf # is the node a leaf
        self.root = root # is the node the root
        self.move = move # the move chosen
        self.game_state = game_state  # the resulted game state
        self.value =  None # the value that minimax compute
        
        self.alpha = 0
        self.beta = 0 
        
        self.parent = None # parent node 
        self.childs = [] # list of child nodes
        
    def add_child(self, node):
        self.childs.append(node)
        node.parent = self
    
    