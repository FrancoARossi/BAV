class Matrix:
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes + 1
        self.n_resources = n_resources + 1
        
    
    def drawMatrix(self):
        noFill()
        strokeWeight(2)
        for p in range(0, self.n_processes):
            for r in range(0, self.n_resources):
                rect(700+(35*p), 80+(35*r), 35, 35)
        

m = Matrix(3, 3)

def setup():
    size(1150, 650)
    frameRate(30.0)
    background(0, 200, 255)
    stroke(0)
    font = loadFont("ArialNarrow-32.vlw")


def draw():
    m.drawMatrix()
