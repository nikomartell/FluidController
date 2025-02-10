import calcs

class CommandSet:
    def __init__(self, component, flowRate, strokes, acceleration, flowDirection, duration, iterations):
        self.component = component
        self.flowRate = int(flowRate) if flowRate is not '' else 500
        self.strokes = int(strokes) if strokes is not '' else 10
        self.acceleration = int(acceleration) if acceleration is not '' else 10
        self.flowDirection = flowDirection
        self.duration = int(duration) if duration is not '' else 3
        self.iterations = int(iterations) if iterations is not '' else 1

    