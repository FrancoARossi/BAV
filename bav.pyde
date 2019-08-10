MATRIX_X = 850
MATRIX_Y = 80
DISTANCE = 60

class PRMatrix:
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes
        self.n_resources = n_resources
    
    def drawMatrix(self):
        noFill()
        strokeWeight(1.5)
        
        rect(MATRIX_X, MATRIX_Y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        if (self.n_processes > 1 and self.n_resources > 1):
            for i in range(1, self.n_processes):
                line(MATRIX_X - DISTANCE, MATRIX_Y + (DISTANCE * i), MATRIX_X + self.n_resources * DISTANCE, MATRIX_Y + (DISTANCE * i))
            
            for j in range(1, self.n_resources):
                line(MATRIX_X + (DISTANCE * j), MATRIX_Y - DISTANCE, MATRIX_X + (DISTANCE * j), MATRIX_Y + self.n_processes * DISTANCE)
        
        
class TextBox:
    def drawTextBox(self):
        fill(255)
        strokeWeight(1)
        rect(525, 275, 100, 100) #Maybe use __init__ for adjustable size
        
    def printKey(self):
        fill(0)
        textSize(50)
        text(key, 560, 345)


textbox = TextBox()

vars = {
        "state" : 0,
        "processes" : 0,
        "resources" : 0
        }

def setup():
    size(1150, 650)
    frameRate(30.0)
    background(0, 200, 255)
    stroke(0)
    
    font = loadFont("ArialNarrow-32.vlw")

def draw():
    
    background(0, 200, 255)
    
    if (vars["state"] == 0):
        textbox.drawTextBox()
        
        if key.isdigit():
            vars["processes"] = int(key)
            textbox.printKey()
    
        if (key == ENTER or key == RETURN):
            vars["state"] = 1
    
    if (vars["state"] == 1):
        textbox.drawTextBox()
        
        if key.isdigit():
            vars["resources"] = int(key)
            textbox.printKey()

        # TODO: FIX. At this point key always equals ENTER (because of the last ENTER pressed)
        if (key == ENTER or key == RETURN):
            vars["state"] = 2
