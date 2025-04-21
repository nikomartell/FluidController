from Controller.Controller import Controller
class CommandSet:
    def __init__(self, speed=500, strokes=0, acceleration=10, flow_direction="Dispense", duration=5, iterations=1, position='', controller=None):
        self.speed = int(speed) if speed != '' else 500
        self.strokes = int(strokes) if strokes != '' else 0
        self.acceleration = int(acceleration) if acceleration != '' else 10
        self.flow_direction = flow_direction
        self.duration = float(duration) if duration != '' else 5
        self.iterations = int(iterations) if iterations != '' else 1
        self.position = 0
        if position == '':
            if isinstance(controller, Controller):
                self.position = controller.linear.get_actual_position()
        else:
            self.position = int(position) if position != '' else 0
        
    def print(self):
        print(f'Speed: {self.speed}')
        print(f'Strokes: {self.strokes}')
        print(f'Acceleration: {self.acceleration}')
        print(f'Flow Direction: {self.flow_direction}')
        print(f'Duration: {self.duration}')
        print(f'Iterations: {self.iterations}')
        print(f'Linear Position: {self.position}')
    
    def array(self):
        return [self.speed, self.strokes, self.acceleration, self.flow_direction, self.duration, self.iterations, self.position]

    def importSet(self, set):
        self.speed = set[0]
        self.strokes = set[1]
        self.acceleration = set[2]
        self.flow_direction = set[3]
        self.duration = set[4]
        self.iterations = set[5]
        self.position = set[6]