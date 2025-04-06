# Notes:
    # From Marie:
        # I was just thinking about the nozzle adjustor subassembly that we are eventually going to build. When the user sets the height for the nozzle to be placed at, the controller needs to do the math to figure out how to angle the nozzle to make sure the fluid makes it onto the slide. Rather than going based off specific flow characteristics, I was thinking that we could have a dropdown or something that lets users select if the flow velocity is slow, medium, or fast, and the controller uses that to do its calculations. Its pretty far down the road, but do you think that would be alright? It would simplify things for both user and developer (you)

https://www.pythonguis.com/faq/real-time-change-of-widgets/
https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
https://realpython.com/python-pyqt-qthread/
https://doc.qt.io/qtforpython-5/PySide2/QtCore/QThreadPool.html


# To-Do
    - Calibrate Rotary Motor
        - Tools Menu
        - Opens window to set 0
        - User moves motor by holding right key
        - Shows current position
        - Spacebar sets 0
        - User moves around the motor until 0
        - Sets Mod to value (Current position % limit value)
    - Pi connections made in seperate file
    - Refactor how Motors are handled
        - Linear ONLY adjusts volume per rotation (Vpr)
        - Command set should only apply to Rotary Motor

# Build with "auto-py-to-exe" in console