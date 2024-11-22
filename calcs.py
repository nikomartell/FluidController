
def setComponent(component):
    return component

def setFlowRate(flowRate):
    if flowRate == '':
        flowRate = 1.0
    return flowRate
    
def setStrokes(strokes):
    if strokes == '':
        strokes = 10
    return strokes
    
def setAcceleration(acceleration):
    if acceleration == '':
        acceleration = 1.0
    return acceleration
    
def setFlowDirection(flowDirection):
    return flowDirection
    
def setDuration(duration):
    if duration == '':
        duration = 10
    return duration

def setIterations(iterations):
    if iterations == '':
        iterations = 10
    return iterations