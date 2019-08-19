#####Global variables#####

GLOBAL_X = 80
GLOBAL_Y = 80
DISTANCE = 30

vars = {
        "current_state" : 0,
        "valid_input" : False
        }

objects = {}

#####Classes#####

class Matrix(object):
    
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.vals = []
        self.row_counter = 0
        self.column_counter = 0
        self.is_renderable = False
    
    def initObject(self):
        for row in range(0, self.n_processes):
            self.vals.append([])
            for column in range(0, self.n_resources):
                self.vals[row].append('')
    
    def __iter__(self):
        self.r = 0
        self.c = 0
        return self
    
    def next(self):
        if self.r < self.n_processes:
            if self.c < self.n_resources:
                ret = self.vals[self.r][self.c]
                if (self.c == (self.n_resources - 1)):
                    self.r += 1
                    self.c = 0
                self.c += 1
                return ret
        else:
            raise StopIteration
    
    # Returns an already initialized matrix with the results of the substractions (no need to use initObject())    
    def __sub__(self, other):
        tmp_matrix = NeededMatrix(self.n_processes, self.n_resources)
        tmp_matrix.initObject()
        for r in range(0, self.n_processes):
            for c in range(0, self.n_resources):
                tmp_matrix.vals[r][c] = self.vals[r][c] - other.vals[r][c]
        return tmp_matrix

class MaxMatrix(Matrix):
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        
        text("Maximum", GLOBAL_X - DISTANCE, GLOBAL_Y - DISTANCE - 10)
        rect(GLOBAL_X, GLOBAL_Y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, GLOBAL_Y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, GLOBAL_Y + (DISTANCE * i))
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), GLOBAL_Y - DISTANCE, GLOBAL_X + (DISTANCE * j), GLOBAL_Y + self.n_processes * DISTANCE)
                
            for i in range(0, self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, GLOBAL_Y + DISTANCE * (i+1) - 5)
            for j in range(0, self.n_resources):
                text("R" + str(j+1), GLOBAL_X + DISTANCE * j + 3, GLOBAL_Y - 10)
            
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.row_counter][self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.column_counter < self.n_resources):
                self.column_counter += 1
            if (self.column_counter == self.n_resources and self.row_counter < self.n_processes):
                self.row_counter += 1
                self.column_counter = 0
            if (self.row_counter == self.n_processes):
                vars["current_state"] = 5
                objects["alloc_matrix"].is_renderable = True
            vars["valid_input"] = False
    
    def printValues(self):
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (GLOBAL_Y + 25) + (DISTANCE * i))

class AllocMatrix(Matrix):
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        alloc_matrix_y = GLOBAL_Y + self.n_processes*DISTANCE + 80
        
        text("Allocated", GLOBAL_X - DISTANCE, alloc_matrix_y - DISTANCE - 10)
        rect(GLOBAL_X, alloc_matrix_y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, alloc_matrix_y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, alloc_matrix_y + (DISTANCE * i))
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), alloc_matrix_y - DISTANCE, GLOBAL_X + (DISTANCE * j), alloc_matrix_y + self.n_processes * DISTANCE)
            
            for i in range(0, self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, alloc_matrix_y + DISTANCE * (i+1) - 5)
            for j in range(0, self.n_resources):
                text("R" + str(j+1), GLOBAL_X + DISTANCE * j + 3, alloc_matrix_y - 10)
    
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.row_counter][self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.vals[self.row_counter][self.column_counter] > objects["max_matrix"].vals[self.row_counter][self.column_counter]):
                raise Exception("Can't allocate more resources than needed")
            if (self.column_counter < self.n_resources):
                self.column_counter += 1
            if (self.column_counter == self.n_resources and self.row_counter < self.n_processes):
                self.row_counter += 1
                self.column_counter = 0
            if (self.row_counter == self.n_processes):
                vars["current_state"] = 6
            vars["valid_input"] = False
    
    def printValues(self):
        alloc_matrix_y = GLOBAL_Y + self.n_processes*DISTANCE + 80
        
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (alloc_matrix_y + 25) + (DISTANCE * i))
            
class NeededMatrix(Matrix):
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        need_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        text("Needed", GLOBAL_X - DISTANCE, need_matrix_y - DISTANCE - 10)
        rect(GLOBAL_X, need_matrix_y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, need_matrix_y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, need_matrix_y + (DISTANCE * i))
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), need_matrix_y - DISTANCE, GLOBAL_X + (DISTANCE * j), need_matrix_y + self.n_processes * DISTANCE)
            
            for i in range(0, self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, need_matrix_y + DISTANCE * (i+1) - 5)
            for j in range(0, self.n_resources):
                text("R" + str(j+1), GLOBAL_X + DISTANCE * j + 3, need_matrix_y - 10)
    
    def printValues(self):
        need_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (need_matrix_y + 25) + (DISTANCE * i))

class TotalVector(object):
    
    def __init__(self, n_processes, n_resources):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.column_counter = 0
        self.vals = []
        self.vector_y = GLOBAL_Y
        self.vector_x = GLOBAL_X + DISTANCE*self.n_resources + 50
        self.is_renderable = True
    
    def initObject(self):
        for i in range(0, self.n_resources):
            self.vals.append('')
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        
        text("Total", self.vector_x, self.vector_y - DISTANCE - 10)
        rect(self.vector_x, self.vector_y, self.n_resources*DISTANCE, DISTANCE)
        if (self.n_resources >= 1):
            for i in range(1, self.n_resources):
                line(self.vector_x + (DISTANCE * i), self.vector_y + DISTANCE, self.vector_x + (DISTANCE * i), self.vector_y - DISTANCE)
            
            for j in range(0, self.n_resources):
                text("R" + str(j+1), self.vector_x + DISTANCE * j + 3, self.vector_y - 10)
    
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.column_counter < (self.n_resources - 1)):
                self.column_counter += 1
            else:
                vars["current_state"] = 4
                objects["max_matrix"].is_renderable = True
            vars["valid_input"] = False
    
    def printValues(self):
        
        for i in range(0, self.n_resources):
            fill(0)
            textSize(25)
            text(self.vals[i], (self.vector_x + 8) + (DISTANCE * i), self.vector_y + 25)
            

class AvailableVector(object):
    
    def __init__(self, n_processes, n_resources):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.column_counter = 0
        self.vals = []
        self.vector_y = GLOBAL_Y + self.n_processes*DISTANCE + 80
        self.vector_x = GLOBAL_X + DISTANCE*self.n_resources + 50
        self.is_renderable = True
    
    def initObject(self, total_vector, alloc_matrix):
        for i in range(0, alloc_matrix.n_resources):
            alloc = 0
            for j in range(0, alloc_matrix.n_processes):
                alloc = alloc + alloc_matrix.vals[j][i]
            val = total_vector.vals[i] - alloc
            if (val < 0):
                raise Exception("Theres more resources allocated than the total")
            self.vals.append(val)
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        
        text("Available", self.vector_x, self.vector_y - DISTANCE - 10)
        rect(self.vector_x, self.vector_y, self.n_resources*DISTANCE, DISTANCE)
        if (self.n_resources >= 1):
            for i in range(1, self.n_resources):
                line(self.vector_x + (DISTANCE * i), self.vector_y + DISTANCE, self.vector_x + (DISTANCE * i), self.vector_y - DISTANCE)
            
            for j in range(0, self.n_resources):
                text("R" + str(j+1), self.vector_x + DISTANCE * j + 3, self.vector_y - 10)
    
    def printValues(self):
        for i in range(0, self.n_resources):
            fill(0)
            textSize(25)
            text(self.vals[i], (self.vector_x + 8) + (DISTANCE * i), self.vector_y + 25)
    
class InputBox(object):
    def __init__(self, next_state = 0):
        self.value = 1
        self.next_state = next_state
        
    def render(self):
        fill(255)
        strokeWeight(1)
        rect(525, 275, 100, 100)
    
    def readValue(self):
        if (key.isdigit() and key != '0' and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.value = int(key)
    
        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            vars["current_state"] = self.next_state
            vars["valid_input"] = False
        
    def printValue(self):
        fill(0)
        textSize(50)
        text(self.value, 560, 345)

#####MAIN#####

vars["input_processes"] = InputBox(1)
vars["input_resources"] = InputBox(2)

def renderObjects():
    for object in objects.values():
            if object.is_renderable:
                object.render()
                object.printValues()

def setup():
    
    size(1150, 650)
    frameRate(24.0)
    background(0, 200, 255)
    stroke(0)
    
    font = loadFont("ArialNarrow-32.vlw")

def draw():
    
    background(0, 200, 255)
    #DEBUG
    print(vars["current_state"])
    
    #Read amount of processes
    if (vars["current_state"] == 0):
        vars["input_processes"].render()
        vars["input_processes"].readValue()
        vars["input_processes"].printValue()
    
    #Read amount of resources
    if (vars["current_state"] == 1):
        vars["input_resources"].render()
        vars["input_resources"].readValue()
        vars["input_resources"].printValue()
    
    #Instanciate objects
    if (vars["current_state"] == 2):
        objects["total_vector"] = TotalVector(vars["input_processes"].value, vars["input_resources"].value)
        objects["max_matrix"] = MaxMatrix(vars["input_processes"].value, vars["input_resources"].value)
        objects["alloc_matrix"] = AllocMatrix(vars["input_processes"].value, vars["input_resources"].value)
        for object in objects.values():
            object.initObject()
        renderObjects()
        vars["current_state"] = 3
        
    
    #Read total_vector values
    if (vars["current_state"] == 3):
        renderObjects()
        objects["total_vector"].readValues()
    
    #Read max_matrix values
    if (vars["current_state"] == 4):
        renderObjects()
        objects["max_matrix"].readValues()
        
    #Read alloc_matrix values
    if (vars["current_state"] == 5):
        renderObjects()
        objects["alloc_matrix"].readValues()
    
    #available_vector instanciation
    if (vars["current_state"] == 6):
        objects["available_vector"] = AvailableVector(objects["total_vector"].n_processes, objects["total_vector"].n_resources)
        objects["available_vector"].initObject(objects["total_vector"], objects["alloc_matrix"])
        renderObjects()
        vars["current_state"] = 7
    
    #needed_matrix creation
    if (vars["current_state"] == 7):
        renderObjects()
        objects["needed_matrix"] = objects["max_matrix"] - objects["alloc_matrix"]
        objects["needed_matrix"].is_renderable = True
        vars["current_state"] = 8
    
    #Show matrixes and vectors
    if (vars["current_state"] == 8):
        renderObjects()
