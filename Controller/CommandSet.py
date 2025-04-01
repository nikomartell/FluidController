class CommandSet:
    def __init__(self, component="Rotary Motor", speed=500, strokes=10, acceleration=10, flowDirection="Dispense", duration=3, iterations=1):
        self.component = component
        self.speed = int(speed) if speed != '' else 500
        self.strokes = int(strokes) if strokes != '' else 10
        self.acceleration = int(acceleration) if acceleration != '' else 10
        self.flowDirection = flowDirection
        self.duration = int(duration) if duration != '' else 3
        self.iterations = int(iterations) if iterations != '' else 1
        
    def print(self):
        print(f'Component: {self.component}')
        print(f'Speed: {self.speed}')
        print(f'Strokes: {self.strokes}')
        print(f'Acceleration: {self.acceleration}')
        print(f'Flow Direction: {self.flowDirection}')
        print(f'Duration: {self.duration}')
        print(f'Iterations: {self.iterations}')

    