class Buttonhandler:


    def buttonPressed(self, name):
        # Handle button press event
        if name == "green_button":
            # Do something when the green button is pressed
            print("Green button pressed")
        elif name == "red_button":
            # Do something when the red button is pressed
            print("Red button pressed")

    def buttonReleased(self, name):
        # Handle button release event
        if name == "green_button":
            # Do something when the green button is released
            print("Green button released")
        elif name == "red_button":
            # Do something when the red button is released
            print("Red button released")
