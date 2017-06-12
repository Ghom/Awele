from ViewManager import *
from EventManager import *
from Controllers import *

def main():
        """..."""
        event_manager = EventManager()

        view_manager = ViewManager( event_manager )

        # No keyboard needed for now
        #keybd = KeyboardController( event_manager )
        mousse = MousseController ( event_manager ) 
        spinner = CPUSpinnerController( event_manager )

        spinner.run()

if __name__ == "__main__":
        main()
