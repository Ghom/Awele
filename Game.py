"""
File name: Game.py 
Description: This file contain the game model used to play the African board game called Awele.
This the game receive event comming from the view (through the EventManager and emit events using the same process
to communicate with the outside world. 
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

from EventManager import *
from Global import Debug

#------------------------------------------------------------------------------
class Game:
        """Game is the model that hold the rules for the game
        and process the necessary actions acording the incoming events
        """
        def __init__(self, event_manager):
            self.event_manager = event_manager
            self.event_manager.register_listener( self )

            # Initialise the pits and stores and create a list for each player
            self.init_containers()
            
            # Create players and assign them a pit list
            self.player1 = Player("Player 1", self.p1_containers)
            self.player2 = Player("Player 2", self.p2_containers)
            self.active_player = self.player1
            self.inactive_player = self.player2
            self.winner = None

            self.play_again = False

            self.event_manager.post(GameStartedEvent(self))
            self.event_manager.post(TextInfoEvent("The game has started, this is Player 1 turn"))
        
        #---------------------------------------------------------------------
        def init_containers(self):
            """init_containers create two linked list of containers containing 6 pits and one store.
            The both list added together create a circular linked list where the store of each list
            is pointing to the first pit of the other list
            """

            # Start creating each list with the final item of the list: the store
            p1_store = Store(self.event_manager, None)
            p2_store = Store(self.event_manager, None)
            self.p1_containers = [p1_store]
            self.p2_containers = [p2_store]
            
            # Then Construct each list in reverse order in a way that each new item added to the
            # list would point to the previous one. (store <- pit6 <- pit5 <- ... <- pit1)
            p1_next = p1_store
            p2_next = p2_store
            for i in range(6,0,-1):
                p1_next = pit_p1 = Pit(self.event_manager, i-1, p1_next)
                p2_next = pit_p2 = Pit(self.event_manager, i-1, p2_next)
                self.p1_containers.insert(0, pit_p1)
                self.p2_containers.insert(0, pit_p2)
            
            # Finally close the loop by making each store pointing at the first pit of the other list
            p1_store.next = self.p2_containers[0]
            p2_store.next = self.p1_containers[0]
            
        #----------------------------------------------------------------------
        def end_turn(self, container):
            """end_turn define the action to be executed after a player ended an action
            """
            # Clear the text info box 
            self.event_manager.post(TextInfoEvent(""))
            self.apply_rules(container)
            
            # If the player is alowed to play again don't do anything
            # otherwise swap the active player with the inactive one
            if self.play_again == False:
                self.active_player, self.inactive_player = self.inactive_player, self.active_player
            else:
                self.play_again = False
                
            Debug("Active player:",self.active_player.name)
            self.event_manager.post(TextInfoEvent("["+self.active_player.name+"]", True))

        #----------------------------------------------------------------------
        def end_game(self):
            """end_game is triggered when the game detect that the end condition is respected
            Condition: The game end when one of the player doesn't have any seeds remaning i his pits
            Action: All the remaining seeds of the other players are transfered to his store
            This assume that the active player triggered the condition thus the only player possesing
            seeds in his pits is the inactive player
            """
            Debug("This is the end of the game!")
            
            # Getting the remaining seeds of the inactive player
            # and putting them in his store
            remaining_seeds = 0
            for container in self.inactive_player.pit_list:
                if not isinstance(container, Store):
                    remaining_seeds += container.take_seeds()
                else:
                    container.add_seed(remaining_seeds)

            # Comparing the two players seeds number to determine who won the game
            # Note: in case of draw self.winner remain the value None otherwise it will point the right player
            if self.player1.pit_list[6].seeds != self.player2.pit_list[6].seeds:
                self.winner = self.player1 if self.player1.pit_list[6].seeds > self.player2.pit_list[6].seeds else self.player2

            # Send the end of game event so the view can change
            self.event_manager.post(EndGameEvent(self))
            
        #---------------------------------------------------------------------
        def apply_rules(self, last_pit):
            """apply_rules is performed after each turn (a turn doesn't always mean a change of active player)
            """
            pit_list_active = self.active_player.pit_list
            pit_list_inactive = self.inactive_player.pit_list
            
            # special rules only apply if the last seed ended in one of the active player containers
            if last_pit in pit_list_active:
                
                # RULE: LAST SEED IN STORE
                if isinstance(last_pit, Store):
                    # each player only have one Store
                    Debug("SPECIAL: Player last seed ended in his own Store he can play again")
                    self.event_manager.post(TextInfoEvent("Your last seed ended in your Store, play again "))
                    self.play_again = True
                
                #RULE: LAST SEED IN EMPTY PIT
                elif last_pit.seeds == 1:
                    # means that the last seed ended in an empty pit of his own
                    Debug("SPECIAL: Player last seed ended in an empty pit of his own he can put the content of the opposite pit plus de last seed in his Store")
                    self.event_manager.post(TextInfoEvent("Your last seed ended in one of your empty pit"))
                    opposite_pit = pit_list_inactive[5 - last_pit.id]
                    # collect the seeds of the opposite pit and put them in your store
                    collected_seeds = opposite_pit.take_seeds() + last_pit.take_seeds()
                    store = pit_list_active[len(pit_list_active)-1]
                    store.add_seed(collected_seeds)

            # END OF GAME CONDITION
            # Check for the end of Game condition: if the active player have no seeds in his pits the game stop
            for container in pit_list_active:
                if isinstance(container, Pit) and container.seeds != 0:
                    break
                    # Player stil have seeds this is not the end of game
                if isinstance(container, Store):
                    # All the pits are empty (because we didn't break on previous condition)
                    # So this is the end of the Game the other player get all the seeds from his pits and put them in his Store
                    self.end_game()
                    return

        #----------------------------------------------------------------------
        def pit_clicked(self, pit):
                """pit_clicked
                """
                # If a pit is clicked check if that pit belong to the active player ...
                if pit in self.active_player.pit_list:
                    if not pit.distribute():
                        # ... and distribute the seeds if the pit is not empty
                        Debug("This pit is empty choose another one")
                        self.event_manager.post(TextInfoEvent("This pit is empty choose another one"))
                else:
                    Debug("This pit doesn't belong to you")
                    self.event_manager.post(TextInfoEvent("This pit doesn't belong to you"))
                    
        #----------------------------------------------------------------------
        def notify(self, event):
            """notify is the incoming point of events reception
            """ 
            if isinstance(event, PitClickedEvent ):
                self.pit_clicked(event.pit)
            
            if isinstance(event, SeedDistributionCompleteEvent ):
                self.end_turn(event.container)
                
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
            if self.seeds == 0:
                Debug("Can't distribute this pit is empty")
                return False
                #need to create exeption for that
                
            seeds = self.seeds
            self.seeds = 0
            Debug("Distribute",seeds,"from pit",self.id)
            Debug("Pit",self.id,"now contain",self.seeds,"seeds")
            self.next.pass_seeds(seeds)
            return True
                        
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

