"""
File name: main.pyw
Description: This file is the main entry point for the game Awele it simply
start the event manager and register the different controlers and views(ViewManager).
The game itself will be started by the view manager.
Author: Guillaume Paniagua
Creation date: 13/06/2017
"""

from ViewManager import *
from ViewManager_terminal import *
from EventManager import *
from Controllers import *
from Global import *

def main():
        event_manager = EventManager()

        if(UI_TYPE == GRAPHIC_UI):
            view_manager = ViewManager( event_manager )

            # No keyboard needed for now.
            # The keyboard events tracking was clearing the mousses events. 
            # The quick fix was to remove it but this need to be look into for future.
            #keybd = KeyboardController( event_manager )
            mousse = MousseController ( event_manager ) 
            spinner = CPUSpinnerController( event_manager )

            # this will trigger the main loop
            spinner.run()
            
        elif(UI_TYPE == CONSOL_UI):
            view_manager = ViewManager_terminal( event_manager )

if __name__ == "__main__":
        main()
