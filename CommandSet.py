import calcs

class CommandSet:
    def __init__(self, component, flowRate, strokes, acceleration, flowDirection, duration, iterations):
        self.component = component
        self.flowRate = calcs.calcFlowRate(flowRate) if flowRate is not None else calcs.calcFlowRate(10.0)
        self.strokes = strokes if strokes is not None else 10
        self.acceleration = acceleration if acceleration is not None else 0.0
        self.flowDirection = flowDirection
        self.duration = duration if duration is not None else 10
        self.iterations = iterations if iterations is not None else 1

    