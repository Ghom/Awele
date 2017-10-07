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
        and process the necessary actions acording to the incoming events
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
            
            # giving the remaining seeds to the player it belong to
            # and putting them in his store
            # Note: Because of the nature of the end of game condition this should only affect one player
            active_player_remaining_seeds = 0
            inactive_player_remaining_seeds = 0
            for active_player_pit, inactive_player_pit in zip(self.active_player.pit_list, self.inactive_player.pit_list):
                if not isinstance(active_player_pit, Store):
                    active_player_remaining_seeds += active_player_pit.take_seeds()
                else:
                    active_player_pit.add_seed(active_player_remaining_seeds)
                    
                if not isinstance(inactive_player_pit, Store):
                    inactive_player_remaining_seeds += inactive_player_pit.take_seeds()
                else:
                    inactive_player_pit.add_seed(inactive_player_remaining_seeds)

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
            active_player_seed_left = 0
            inactive_player_seed_left = 0
            for container_active, container_inactive in zip(pit_list_active, pit_list_inactive):
                if isinstance(container_active, Pit):
                    active_player_seed_left += container_active.seeds
                
                if isinstance(container_inactive, Pit):
                    inactive_player_seed_left += container_inactive.seeds
                
                # if both player still have seeds left this is won't trigger end of game 
                # so the loop can stop to avoid wasting time (even if this not a big deal there)
                if (active_player_seed_left != 0) and (inactive_player_seed_left != 0):
                    break;
                    
            if (active_player_seed_left == 0) or (inactive_player_seed_left == 0):
                # on of the side is completely empty
                # So this is the end of the Game the other player get all the seeds from his pits and put them in his Store
                self.end_game()
                return

        #----------------------------------------------------------------------
        def pit_clicked(self, pit):
                """pit_clicked is a game method executed when a PitClickedEvent
				occurs. The method will execute the right action depending on
				the pit that has been clicked and the active player.
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
        """Container is Abstract class that represent the board container 
		common feature such as a Pit or a Store 
		"""
        def __init__(self):
            self.event_manager = None
            self.next = None
            self.seeds = 0

        #----------------------------------------------------------------------
        def pass_seeds(self, seeds):
            """pass_seeds method is used to get on seed from the incoming
            seeds and pass the rest to the next container.
            This method is called from container to container going through 
            the circular linked list until there is no seed left. This represent the player's hand 
            distributing the seeds around the board.
            """
            # This method assume that the incoming seeds parameter is always more than 0
            # This assumption can be made because the previous container would have
            # check the remaining seed number before passing to the next container
            self.add_seed(1) # get one seed ...
            seeds -= 1 # ... from the seeds passing around

            if isinstance(self, Pit):
                Debug("Pit",self.id,"now contain",self.seeds,"seeds")
            else:
                Debug("Store now contain",self.seeds,"seeds")

            # here we check that there is still seeds to pass$ around before passing
            if seeds > 0:
                self.next.pass_seeds(seeds)
            else:
                self.event_manager.post(SeedDistributionCompleteEvent(self))

        #----------------------------------------------------------------------
        def add_seed(self, amount):
            """add_seed add an amount of seed to the container
            parameters:
            amount -- integer number of seeds that need to be added to the container
            """
            self.seeds += amount
            return self.seeds 

        #----------------------------------------------------------------------
        def remove_seed(self, amount):
            """remove_seed remove an amount of seed to the container
            parameters:
            amount -- integer number of seeds that need to be removed from the container
            """
            self.seeds -= amount
            return self.seeds

        #----------------------------------------------------------------------
        def take_seeds(self):
            """take_seeds remove all seeds in the container and return that number
            of seeds that was in the container
            return -- integer amount of seeds that was present in the container
            (represent the player's hand taking all the seeds)
            """
            amount = self.seeds
            self.seeds = 0
            return amount
            
#------------------------------------------------------------------------------
class Pit(Container):
            """Pit class is a subclass of Container and describe the specificities of pits"""
            def __init__(self, event_manager, id_nb, next_container):
                Container.__init__(self)
                self.event_manager = event_manager

                self.id = id_nb
                self.next = next_container
                self.seeds = 6

            def distribute(self):
                """distribute method is the starting point of passing the seeds around to other containers"""
                if self.seeds == 0:
                    Debug("Can't distribute this pit is empty")
                    return False
                    #TODO: need to create exeption for that
                    
                seeds = self.take_seeds()
                Debug("Distribute",seeds,"from pit",self.id)
                Debug("Pit",self.id,"now contain",self.seeds,"seeds")
                self.next.pass_seeds(seeds)
                return True
                        
#------------------------------------------------------------------------------
class Store(Container):
            """Store class is a subclass of Container and describe the specificities of stores"""
            def __init__(self, event_manager, next_container):
                Container.__init__(self)
                self.event_manager = event_manager
                
                self.next = next_container

#------------------------------------------------------------------------------
class Player:
            """Player class hold the player data"""
            def __init__(self, name, pit_list=None):
                self.name = name
                self.score = 0
                self.pit_list = pit_list

