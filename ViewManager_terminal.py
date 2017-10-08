"""
File name: ViewManager_terminal.py
Description: This file is the equivalent of the UI game but in console
this is intended to be for testing only and abstraction of UI.
Author: Guillaume Paniagua
Creation date: 07/10/2017
"""
from EventManager import *
from Game import *
from AI_player import * 
import sys

class ViewManager_terminal:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        
        self.game = Game(self.event_manager)
        self.computer = AI_player(self.event_manager, self.game)
        self.draw_board()
        self.select_pit()
    
    def draw_board(self):
        top_pit1, top_pit2, top_pit3, top_pit4, top_pit5, top_pit6, top_bank = [pit.seeds for pit in self.game.player2.pit_list]
        bot_pit1, bot_pit2, bot_pit3, bot_pit4, bot_pit5, bot_pit6, bot_bank = [pit.seeds for pit in self.game.player1.pit_list]
        
        print(" ---------------------------------------------------------------")
        print("|",          "\t|",top_pit6, "\t|",top_pit5, "\t|",top_pit4, "\t|",top_pit3, "\t|",top_pit2, "\t|",top_pit1, "\t|",          "\t|",)
        print("|",top_bank, "\t|",          "\t|",          "\t|",          "\t|",          "\t|",          "\t|"           "\t|",bot_bank, "\t|",)
        print("|",          "\t|",bot_pit1, "\t|",bot_pit2, "\t|",bot_pit3, "\t|",bot_pit4, "\t|",bot_pit5, "\t|",bot_pit6, "\t|",          "\t|",)
        print(" ---------------------------------------------------------------")
    
    def select_pit(self):
        sel_pit = input("What pit do you want to select? ")
        self.event_manager.post(PitClickedEvent(self.game.active_player.pit_list[int(sel_pit)-1]))

        
    #----------------------------------------------------------------------
    def notify(self, event):
        """notify is the incoming point of events reception
        """
        if isinstance(event, GameStartedEvent):
            # when the game start "draw" the board and ask for pit selection
            # self.draw_board()
            # self.select_pit()
            pass

        if isinstance(event, TextInfoEvent):
            # print game info
            print(event.text)
            
        if isinstance(event, EndTurnEvent):
            # when the turn is finish "draw" the board and ask for pit selection
            self.draw_board()
            self.select_pit()