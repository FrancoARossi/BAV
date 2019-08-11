MATRIX_X = 850
MATRIX_Y = 80
DISTANCE = 60

vars = {
        "current_state" : 0,
        "valid_input" : False
        }

class MaxMatrix:
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes
        self.n_resources = n_resources
    
    def drawMatrix(self):
        noFill()
        strokeWeight(1.5)
        
        rect(MATRIX_X, MATRIX_Y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        #TODO show processes and resources for each row and column
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(MATRIX_X - DISTANCE, MATRIX_Y + (DISTANCE * i), MATRIX_X + self.n_resources * DISTANCE, MATRIX_Y + (DISTANCE * i))
            
            for j in range(1, self.n_resources):
                line(MATRIX_X + (DISTANCE * j), MATRIX_Y - DISTANCE, MATRIX_X + (DISTANCE * j), MATRIX_Y + self.n_processes * DISTANCE)
    
    def loadValues(self):
        #TODO
        pass
        
class AllocMatrix:
    #TODO
    pass
    
class ReqMatrix:
    #TODO
    pass
        
class InputBox:
    def __init__(self, next_state = 0):
        self.value = ''
        self.next_state = next_state
        
    def drawInputBox(self):
        fill(255)
        strokeWeight(1)
        rect(525, 275, 100, 100) #Maybe use __init__ for adjustable size
    
    def readValue(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.value = int(key)
    
        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            vars["current_state"] = self.next_state
            vars["valid_input"] = False
        
    def printValue(self):
        fill(0)
        textSize(50)
        text(self.value, 560, 345)


input_processes = InputBox(1)
input_resources = InputBox(2)

def setup():
    size(1150, 650)
    frameRate(30.0)
    background(0, 200, 255)
    stroke(0)
    
    font = loadFont("ArialNarrow-32.vlw")

def draw():
    
    background(0, 200, 255)
    
    if (vars["current_state"] == 0):
        input_processes.drawInputBox()
        input_processes.readValue()
        input_processes.printValue()
    
    if (vars["current_state"] == 1):
        input_resources.drawInputBox()
        input_resources.readValue()
        input_resources.printValue()
        
    if (vars["current_state"] == 2):
        max_matrix = MaxMatrix(input_processes.value, input_resources.value)
        #max_matrix.loadValues()
        max_matrix.drawMatrix()
        #alloc_matrix = AllocMatrix()
        #req_matrix = max_matrix - alloc_matrix
