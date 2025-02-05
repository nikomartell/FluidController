# Notes:
    # From Marie:
        # I was just thinking about the nozzle adjustor subassembly that we are eventually going to build. When the user sets the height for the nozzle to be placed at, the controller needs to do the math to figure out how to angle the nozzle to make sure the fluid makes it onto the slide. Rather than going based off specific flow characteristics, I was thinking that we could have a dropdown or something that lets users select if the flow velocity is slow, medium, or fast, and the controller uses that to do its calculations. Its pretty far down the road, but do you think that would be alright? It would simplify things for both user and developer (you)

# To-Do
    - Ensure interruptions are properly handled
        - Force Stop Motor, Closing the window, etc.
    - Implement the Weight Scale
        - Hopefully just getting the drivers will do that
    - Refactor how Motors are handled
        - Both can be used simultaneously, so allow the user to put commands for one or both.
    - Reconsider how the Command Set is structured
        - Certain parameters are not needed / complex.
    - Start working on Calcs for correct measurements
        - Mainly for flowRate
    - Implement sequential sets
        - Probably can just set it as an array of CommandSets