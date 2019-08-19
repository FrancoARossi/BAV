#####Global variables#####

GLOBAL_X = 80
GLOBAL_Y = 80
DISTANCE = 30

vars = {
        "current_state" : 0,
        "valid_input" : False
        }

#####Classes#####

class Matrix(object):
    
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.vals = []
        self.row_counter = 0
        self.column_counter = 0
    
    def initMatrix(self):
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
    
    # Returns an already initialized matrix with the results of the substractions (no need to use initMatrix())    
    def __sub__(self, other):
        tmp_matrix = ReqMatrix(self.n_processes, self.n_resources)
        tmp_matrix.initMatrix()
        for r in range(0, self.n_processes):
            for c in range(0, self.n_resources):
                tmp_matrix.vals[r][c] = self.vals[r][c] - other.vals[r][c]
        return tmp_matrix

class MaxMatrix(Matrix):
    
    def drawMatrix(self):
        noFill()
        strokeWeight(1.5)
        
        rect(GLOBAL_X, GLOBAL_Y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        #TODO show processes and resources for each row and column
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, GLOBAL_Y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, GLOBAL_Y + (DISTANCE * i))
            
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), GLOBAL_Y - DISTANCE, GLOBAL_X + (DISTANCE * j), GLOBAL_Y + self.n_processes * DISTANCE)
    
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
                vars["current_state"] = 4
            vars["valid_input"] = False
    
    def printValues(self):
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (GLOBAL_Y + 25) + (DISTANCE * i))

class AllocMatrix(Matrix):
    
    def drawMatrix(self):
        noFill()
        strokeWeight(1.5)
        alloc_matrix_y = GLOBAL_Y + self.n_processes*DISTANCE + 80
        
        rect(GLOBAL_X, alloc_matrix_y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        #TODO show processes and resources for each row and column
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, alloc_matrix_y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, alloc_matrix_y + (DISTANCE * i))
            
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), alloc_matrix_y - DISTANCE, GLOBAL_X + (DISTANCE * j), alloc_matrix_y + self.n_processes * DISTANCE)
    
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.row_counter][self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.vals[self.row_counter][self.column_counter] > vars["max_matrix"].vals[self.row_counter][self.column_counter]):
                raise Exception("Can't allocate more resources than needed")
            if (self.column_counter < self.n_resources):
                self.column_counter += 1
            if (self.column_counter == self.n_resources and self.row_counter < self.n_processes):
                self.row_counter += 1
                self.column_counter = 0
            if (self.row_counter == self.n_processes):
                vars["current_state"] = 5
            vars["valid_input"] = False
    
    def printValues(self):
        alloc_matrix_y = GLOBAL_Y + self.n_processes*DISTANCE + 80
        
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (alloc_matrix_y + 25) + (DISTANCE * i))
            
class ReqMatrix(Matrix):
    
    def drawMatrix(self):
        noFill()
        strokeWeight(1.5)
        alloc_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        rect(GLOBAL_X, alloc_matrix_y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        #TODO show processes and resources for each row and column
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, alloc_matrix_y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, alloc_matrix_y + (DISTANCE * i))
            
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), alloc_matrix_y - DISTANCE, GLOBAL_X + (DISTANCE * j), alloc_matrix_y + self.n_processes * DISTANCE)
    
    def printValues(self):
        alloc_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        for i in range(0, self.n_processes):
            for j in range(0, len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (alloc_matrix_y + 25) + (DISTANCE * i))

class TotalVector(object):
    
    def __init__(self, n_processes, n_resources):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.column_counter = 0
        self.vals = []
        self.vector_y = GLOBAL_Y
        self.vector_x = GLOBAL_X + DISTANCE*self.n_resources + 50
    
    def initVector(self):
        for i in range(0, self.n_resources):
            self.vals.append('')
    
    def drawVector(self):
        noFill()
        strokeWeight(1.5)
        
        rect(self.vector_x, self.vector_y, self.n_resources*DISTANCE, DISTANCE)
        if (self.n_resources >= 1):
            for i in range(1, self.n_resources):
                line(self.vector_x + (DISTANCE * i), self.vector_y + DISTANCE, self.vector_x + (DISTANCE * i), self.vector_y - DISTANCE)
    
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.column_counter < (self.n_resources - 1)):
                self.column_counter += 1
            else:
                vars["current_state"] = 3
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
    
    def initVector(self, total_vector, alloc_matrix):
        for i in range(0, alloc_matrix.n_resources):
            alloc = 0
            for j in range(0, alloc_matrix.n_processes):
                alloc = alloc + alloc_matrix.vals[j][i]
            val = total_vector.vals[i] - alloc
            if (val < 0):
                raise Exception("Theres more resources allocated than the total")
            self.vals.append(val)
    
    def drawVector(self):
        noFill()
        strokeWeight(1.5)
        
        rect(self.vector_x, self.vector_y, self.n_resources*DISTANCE, DISTANCE)
        if (self.n_resources >= 1):
            for i in range(1, self.n_resources):
                line(self.vector_x + (DISTANCE * i), self.vector_y + DISTANCE, self.vector_x + (DISTANCE * i), self.vector_y - DISTANCE)
    
    def printValues(self):
        for i in range(0, self.n_resources):
            fill(0)
            textSize(25)
            text(self.vals[i], (self.vector_x + 8) + (DISTANCE * i), self.vector_y + 25)
    
class InputBox(object):
    def __init__(self, next_state = 0):
        self.value = 1
        self.next_state = next_state
        
    def drawInputBox(self):
        fill(255)
        strokeWeight(1)
        rect(525, 275, 100, 100) #Maybe use __init__ for adjustable size
    
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

input_processes = InputBox(1)
input_resources = InputBox(2)

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
    
    # Read amount of processes
    if (vars["current_state"] == 0):
        input_processes.drawInputBox()
        input_processes.readValue()
        input_processes.printValue()
    
    # Read amount of resources and instanciate objects
    if (vars["current_state"] == 1):
        input_resources.drawInputBox()
        input_resources.readValue()
        input_resources.printValue()
        vars["total_vector"] = TotalVector(input_processes.value, input_resources.value)
        vars["total_vector"].initVector()
        vars["max_matrix"] = MaxMatrix(input_processes.value, input_resources.value)
        vars["max_matrix"].initMatrix()
        vars["alloc_matrix"] = AllocMatrix(input_processes.value, input_resources.value)
        vars["alloc_matrix"].initMatrix()
    
    if (vars["current_state"] == 2):
        #TODO
        vars["total_vector"].drawVector()
        vars["total_vector"].readValues()
        vars["total_vector"].printValues()
    
    # Read max_matrix values
    if (vars["current_state"] == 3):
        vars["total_vector"].drawVector()
        vars["total_vector"].printValues()
        vars["max_matrix"].drawMatrix()
        vars["max_matrix"].readValues()
        vars["max_matrix"].printValues()
        
    #Read alloc_matrix values
    if (vars["current_state"] == 4):
        vars["total_vector"].drawVector()
        vars["total_vector"].printValues()
        vars["max_matrix"].drawMatrix()
        vars["max_matrix"].printValues()
        vars["alloc_matrix"].drawMatrix()
        vars["alloc_matrix"].readValues()
        vars["alloc_matrix"].printValues()
    
    if (vars["current_state"] == 5):
        vars["available_vector"] = AvailableVector(vars["total_vector"].n_processes, vars["total_vector"].n_resources)
        vars["available_vector"].initVector(vars["total_vector"], vars["alloc_matrix"])
        vars["available_vector"].drawVector()
        vars["available_vector"].printValues()
        vars["total_vector"].drawVector()
        vars["total_vector"].printValues()
        vars["max_matrix"].drawMatrix()
        vars["max_matrix"].printValues()
        vars["alloc_matrix"].drawMatrix()
        vars["alloc_matrix"].printValues()
        vars["current_state"] = 6
    
    #req_matrix instanciation
    if (vars["current_state"] == 6):
        vars["total_vector"].drawVector()
        vars["total_vector"].printValues()
        vars["available_vector"].drawVector()
        vars["available_vector"].printValues()
        vars["max_matrix"].drawMatrix()
        vars["max_matrix"].printValues()
        vars["alloc_matrix"].drawMatrix()
        vars["alloc_matrix"].printValues()
        vars["req_matrix"] = vars["max_matrix"] - vars["alloc_matrix"]
        vars["current_state"] = 7
    
    #Show matrixes and vectors
    if (vars["current_state"] == 7):
        vars["total_vector"].drawVector()
        vars["total_vector"].printValues()
        vars["available_vector"].drawVector()
        vars["available_vector"].printValues()
        vars["max_matrix"].drawMatrix()
        vars["max_matrix"].printValues()
        vars["alloc_matrix"].drawMatrix()
        vars["alloc_matrix"].printValues()
        vars["req_matrix"].drawMatrix()
        vars["req_matrix"].printValues()
