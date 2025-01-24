# Notes:
    # TMCM-1240 test
    # TMCM-3110 triple axis motor
    # Firmware Update the 1140s (1.4.7)
    # Check for update then flash the firmware
    # From Marie:
        # I was just thinking about the nozzle adjustor subassembly that we are eventually going to build. When the user sets the height for the nozzle to be placed at, the controller needs to do the math to figure out how to angle the nozzle to make sure the fluid makes it onto the slide. Rather than going based off specific flow characteristics, I was thinking that we could have a dropdown or something that lets users select if the flow velocity is slow, medium, or fast, and the controller uses that to do its calculations. Its pretty far down the road, but do you think that would be alright? It would simplify things for both user and developer (you)