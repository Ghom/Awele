from EventManager import *
from Global import Debug

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
            self.winner = None

            self.play_again = False

            self.event_manager.post(GameStartedEvent(self))
            self.event_manager.post(TextInfoEvent("The game has started, this is Player 1 turn"))

        #----------------------------------------------------------------------
        def end_turn(self):
            if self.play_again == False:
                self.active_player, self.inactive_player = self.inactive_player, self.active_player
            else:
                self.play_again = False
            Debug("Active player:",self.active_player.name)
            self.event_manager.post(TextInfoEvent("["+self.active_player.name+"]", True))

        #----------------------------------------------------------------------
        def end_game(self):
            Debug("This is the end of the game!")
            remaining_seeds = 0
            for container in self.inactive_player.pit_list:
                if not isinstance(container, Store):
                    # getting the remaining seeds
                    remaining_seeds += container.take_seeds()
                else:
                    #and putting them in the store
                    container.add_seed(remaining_seeds)

            if self.player1.pit_list[6].seeds != self.player2.pit_list[6].seeds:
                self.winner = self.player1 if self.player1.pit_list[6].seeds > self.player2.pit_list[6].seeds else self.player2

            self.event_manager.post(EndGameEvent(self))
            
        #---------------------------------------------------------------------
        def check_special_actions(self, last_pit):
        #This opperation is performed after each turn (a turn doesn't always mean a change of active player)
            
            pit_list_active = self.active_player.pit_list
            pit_list_inactive = self.inactive_player.pit_list
                
            if last_pit in pit_list_active:
                if isinstance(last_pit, Store):
                    # each player only have one Store
                    Debug("SPECIAL: Player last seed ended in his own Store he can play again")
                    self.event_manager.post(TextInfoEvent("Your last seed ended in your Store, play again "))
                    self.play_again = True
                elif last_pit.seeds == 1:
                    # means that the last seed ended in an empty pit of his own
                    Debug("SPECIAL: Player last seed ended in an empty pit of his own he can put the content of the opposite pit plus de last seed in his Store")
                    self.event_manager.post(TextInfoEvent("Your last seed ended in one of your empty pit"))
                    opposite_pit = pit_list_inactive[5 - last_pit.id]
                    
                    collected_seeds = opposite_pit.take_seeds() + last_pit.take_seeds()
                    store = pit_list_active[len(pit_list_active)-1]
                    store.add_seed(collected_seeds)

            # Check for the end of Game condition true if one of the player have no seeds in his pit
            # As the current player is only allowed to move seeds from his side and we assume that
            # This test will be performed after each turn we only need to chack the pits of the active player
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
        def notify(self, event):
            if isinstance(event, PitClickedEvent ):
                if event.pit in self.active_player.pit_list:
                    if not event.pit.distribute():
                        self.play_again == True
                        Debug("This pit is empty choose another one")
                        self.event_manager.post(TextInfoEvent("This pit is empty choose another one"))
                else:
                    Debug("This pit doesn't belong to you")
                    self.event_manager.post(TextInfoEvent("This pit doesn't belong to you"))
            if isinstance(event, SeedDistributionCompleteEvent ):
                self.event_manager.post(TextInfoEvent(""))
                self.check_special_actions(event.container)
                self.end_turn()
