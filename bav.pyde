#####Global variables#####

GLOBAL_X = 80
GLOBAL_Y = 80
DISTANCE = 30

vars = {
        "current_state" : 0,
        "valid_input" : False,
        "safe_sequence" : [],
        "sequence_string" : "",
        "time" : 0,
        "counter" : -1,
        "blocked_units" : [],
        "repeat" : False
        }

objects = []

#####Matrixes#####

class Matrix(object):
    
    def __init__(self, n_processes = 0, n_resources = 0):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.vals = []
        self.row_counter = 0
        self.column_counter = 0
        self.is_renderable = False
    
    def initObject(self):
        for row in range(self.n_processes):
            self.vals.append([])
            for column in range(self.n_resources):
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
        tmp_matrix = NeedMatrix(self.n_processes, self.n_resources)
        tmp_matrix.initObject()
        for r in range(self.n_processes):
            for c in range(self.n_resources):
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
                
            for i in range(self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, GLOBAL_Y + DISTANCE * (i+1) - 5)
            for j in range(self.n_resources):
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
                objects[2].is_renderable = True
            vars["valid_input"] = False
    
    def printValues(self):
        for i in range(self.n_processes):
            for j in range(len(self.vals[i])):
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
            
            for i in range(self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, alloc_matrix_y + DISTANCE * (i+1) - 5)
            for j in range(self.n_resources):
                text("R" + str(j+1), GLOBAL_X + DISTANCE * j + 3, alloc_matrix_y - 10)
    
    def readValues(self):
        if (key.isdigit() and key != ENTER and key != RETURN):
            vars["valid_input"] = True
            self.vals[self.row_counter][self.column_counter] = int(key)

        if ((key == ENTER or key == RETURN) and vars["valid_input"]):
            if (self.vals[self.row_counter][self.column_counter] > objects[1].vals[self.row_counter][self.column_counter]):
                raise Exception("Can't allocate more resources than need")
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
        
        for i in range( self.n_processes):
            for j in range(len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (alloc_matrix_y + 25) + (DISTANCE * i))
            
class NeedMatrix(Matrix):
    
    def render(self):
        noFill()
        textSize(20)
        strokeWeight(1.5)
        need_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        text("Need", GLOBAL_X - DISTANCE, need_matrix_y - DISTANCE - 10)
        rect(GLOBAL_X, need_matrix_y, self.n_resources*DISTANCE, self.n_processes*DISTANCE)
        if (self.n_processes >= 1 and self.n_resources >= 1):
            for i in range(1, self.n_processes):
                line(GLOBAL_X - DISTANCE, need_matrix_y + (DISTANCE * i), GLOBAL_X + self.n_resources * DISTANCE, need_matrix_y + (DISTANCE * i))
            for j in range(1, self.n_resources):
                line(GLOBAL_X + (DISTANCE * j), need_matrix_y - DISTANCE, GLOBAL_X + (DISTANCE * j), need_matrix_y + self.n_processes * DISTANCE)
            
            for i in range(self.n_processes):
                text("P" + str(i+1), GLOBAL_X - DISTANCE, need_matrix_y + DISTANCE * (i+1) - 5)
            for j in range(self.n_resources):
                text("R" + str(j+1), GLOBAL_X + DISTANCE * j + 3, need_matrix_y - 10)
    
    def printValues(self):
        need_matrix_y = GLOBAL_Y + 2*self.n_processes*DISTANCE + 160
        
        for i in range(self.n_processes):
            for j in range(len(self.vals[i])):
                fill(0)
                textSize(25)
                text(self.vals[i][j], (GLOBAL_X + 8) + (DISTANCE * j), (need_matrix_y + 25) + (DISTANCE * i))
                
#####Vectors#####

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
        for i in range(self.n_resources):
            self.vals.append('')
    
    def render(self):
        fill(0)
        textSize(20)
        strokeWeight(1.5)
        
        text("Total", self.vector_x, self.vector_y - DISTANCE - 10)
        noFill()
        rect(self.vector_x, self.vector_y, self.n_resources*DISTANCE, DISTANCE)
        if (self.n_resources >= 1):
            for i in range(1, self.n_resources):
                line(self.vector_x + (DISTANCE * i), self.vector_y + DISTANCE, self.vector_x + (DISTANCE * i), self.vector_y - DISTANCE)
            
            for j in range(self.n_resources):
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
                objects[1].is_renderable = True
            vars["valid_input"] = False
    
    def printValues(self):
        
        for i in range(self.n_resources):
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
        for i in range(alloc_matrix.n_resources):
            alloc = 0
            for j in range(alloc_matrix.n_processes):
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
            
            for j in range(self.n_resources):
                text("R" + str(j+1), self.vector_x + DISTANCE * j + 3, self.vector_y - 10)
    
    def printValues(self):
        for i in range(self.n_resources):
            fill(0)
            textSize(25)
            text(self.vals[i], (self.vector_x + 8) + (DISTANCE * i), self.vector_y + 25)

#####InputBox#####
    
class InputBox(object):
    def __init__(self, next_state, type):
        self.value = 1
        self.next_state = next_state
        self.type = type
        
    def render(self):
        fill(255)
        strokeWeight(1)
        rect(525, 275, 100, 100)
        fill(0)
        textSize(30)
        text(self.type, 500, 200)
    
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

#####Resource Allocation Graph#####

class Resource(object):
    
    def __init__(self, n_resources, units, i_resource):
        self.n_resources = n_resources
        self.units = units
        self.i_resource = i_resource
        self.resource_y = GLOBAL_Y + 80
        self.k = 0
        
        if self.n_resources % 2 == 0:
            if self.i_resource > 1:
                self.k = 3
            else:
                self.k = 1
        else:
            if self.n_resources == 3:
                if self.i_resource == 0:
                    self.k = 0
                elif self.i_resource in range(1, 3):
                    self.k = 2
            else:
                if self.i_resource == 0:
                    self.k = 0
                elif self.i_resource in range(1, 3):
                    self.k = 1.5
                else:
                    self.k = 3
        self.resource_x = GLOBAL_X + 650 + 80*pow(-1, self.i_resource)*self.k
        self.unit_coords = []
        
        for unit in range(self.units):
            if unit == 0:
                c = 0
            elif unit % self.units > 2:
                c = 2
            else:
                c = 1
            self.unit_coords.append((self.resource_x + 40 + 15*c*pow(-1, unit), self.resource_y + 60))
    
    def render(self):
        fill(255, 255, 255)
        strokeWeight(1.5)
        textSize(24)
        ellipseMode(CENTER)
        
        rect(self.resource_x, self.resource_y, 80, 80)
        fill(0)
        text("R" + str(self.i_resource+1), self.resource_x + 25, self.resource_y + 30)
        for x, y in self.unit_coords:
            ellipse(x, y, 10, 10)

class Process(object):
    
    def __init__(self, n_processes, i_process):
        self.n_processes = n_processes
        self.i_process = i_process
        self.process_y = GLOBAL_Y + 420
        self.k = 0
        self.used_units = []
        self.R, self.G, self.B = random(255), random(255), random(255)
        
        if self.n_processes % 2 == 0:
            if self.i_process > 1:
                self.k = 3
            else:
                self.k = 1
        else:
            if self.n_processes == 3:
                if self.i_process == 0:
                    self.k = 0
                elif self.i_process in range(1, 3):
                    self.k = 2
            else:
                if self.i_process == 0:
                    self.k = 0
                elif self.i_process in range(1, 3):
                    self.k = 1.5
                else:
                    self.k = 3
        
        self.process_x = GLOBAL_X + 690 + 80*pow(-1, self.i_process)*self.k
    
    def render(self):
        fill(255, 255, 255)
        strokeWeight(1.5)
        textSize(24)
        ellipseMode(CENTER)
        
        ellipse(self.process_x, self.process_y, 80, 80)
        fill(0)
        text("P" + str(self.i_process+1), self.process_x - 15, self.process_y + 10)
    
    def renderConnections(self, resources, alloc_units, need_units):
        process_top_y = self.process_y - 40
        i = -1
        strokeWeight(4)
        stroke(self.R, self.G, self.B)
        
        for alloc_amount in alloc_units:
            i += 1
            for j in range(alloc_amount):
                available_units = [unit for unit in resources[i].unit_coords if unit not in vars["blocked_units"]]
                if len(available_units) > 0:
                    vars["blocked_units"].append(available_units[0])
                    line(self.process_x, process_top_y, available_units[0][0], available_units[0][1])
        i = -1
        for need_unit in need_units:
            i += 1
            for j in range(need_unit):
                line(self.process_x, process_top_y, resources[i].resource_x + 40, resources[i].resource_y + 80)
        stroke(0)

#####Functions#####

def renderObjects(objects):
    fill(0)
    for object in objects:
            if object.is_renderable:
                object.render()
                object.printValues()

def bankersAlgorithm(objects):
    #objects indexes = 0: TotalVector, 1: MaxMatrix, 2: AllocMatrix, 3: AvailableVector, 4: NeedMatrix
    if vars["counter"] < vars["input_processes"].value:
        if vars["counter"] == -1:
            vars["time"] = millis()
            vars["counter"] += 1
        if (millis() - vars["time"] >= 500):
            if vars["counter"]+1 in vars["safe_sequence"]:
                vars["counter"] += 1
            elif objects[3].vals >= objects[4].vals[vars["counter"]]:
                vars["safe_sequence"].append(vars["counter"]+1)
                for j in range(vars["input_resources"].value):
                    objects[3].vals[j] += objects[2].vals[vars["counter"]][j]
                    objects[2].vals[vars["counter"]][j] = 0
                    objects[4].vals[vars["counter"]][j] = 0
                
                vars["sequence_string"] = "<"
                for j in vars["safe_sequence"]:
                    vars["sequence_string"] += "P" + str(j) + ", "
                vars["sequence_string"] = vars["sequence_string"][:-2]
                vars["sequence_string"] += "> It's a safe sequence"
                vars["counter"] = -1
            else:
                vars["counter"] += 1
        if len(vars["sequence_string"]) > 0:
            background(220, 220, 220)
            drawWatermarkAndExit()
            delay(500)
            renderObjects(objects)
            textSize(20)
            fill(0, 150, 0)
            text(vars["sequence_string"], 600, 100)
            renderRAG(objects)
            vars["blocked_units"] = []
    else:
        vars["current_state"] = 10

def drawWatermarkAndExit():
    github_logo = loadImage("github-logo.png")
    tint(255, 126)
    image(github_logo, 940, 580)
    noTint()
    textSize(18)
    text("Press ESC to exit", 10, 635)
    fill(0, 0, 0 , 126)
    text("FrancoARossi", 1010, 620)

def renderRAG(objects):
    #objects indexes = 0: TotalVector, 1: MaxMatrix, 2: AllocMatrix, 3: AvailableVector, 4: NeedMatrix
    for r in vars["resources"]:
        r.render()
    for i in range(vars["input_processes"].value):
        vars["processes"][i].render()
        vars["processes"][i].renderConnections(vars["resources"], objects[2].vals[i], objects[4].vals[i])

#####MAIN#####

def setup():
    
    size(1150, 650)
    frameRate(24.0)
    background(220, 220, 220)
    stroke(0)
    vars["input_processes"] = InputBox(1, "Processes")
    vars["input_resources"] = InputBox(2, "Resources")
    
    font = loadFont("ArialRoundedMTBold-48.vlw")
    textFont(font)

def draw():
    
    background(220, 220, 220)
    drawWatermarkAndExit()
    
    if (vars["current_state"] > 7):
        renderRAG(objects)
        vars["blocked_units"] = []
    
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
        objects.append(TotalVector(vars["input_processes"].value, vars["input_resources"].value))
        objects[0].initObject()
        objects.append(MaxMatrix(vars["input_processes"].value, vars["input_resources"].value))
        objects[1].initObject()
        objects.append(AllocMatrix(vars["input_processes"].value, vars["input_resources"].value))
        objects[2].initObject()
        renderObjects(objects)
        vars["current_state"] = 3
        
    
    #Read total_vector values
    if (vars["current_state"] == 3):
        objects[0].render()
        objects[0].printValues()
        objects[1].render()
        objects[1].printValues()
        objects[2].render()
        objects[2].printValues()
        objects[0].readValues()
    
    #Read max_matrix values
    if (vars["current_state"] == 4):
        objects[0].render()
        objects[0].printValues()
        objects[1].render()
        objects[1].printValues()
        objects[2].render()
        objects[2].printValues()
        objects[1].readValues()
        
    #Read alloc_matrix values
    if (vars["current_state"] == 5):
        objects[0].render()
        objects[0].printValues()
        objects[1].render()
        objects[1].printValues()
        objects[2].render()
        objects[2].printValues()
        objects[2].readValues()
    
    #available_vector instanciation
    if (vars["current_state"] == 6):
        objects.append(AvailableVector(objects[0].n_processes, objects[0].n_resources))
        objects[3].initObject(objects[0], objects[2])
        objects[0].render()
        objects[0].printValues()
        objects[1].render()
        objects[1].printValues()
        objects[2].render()
        objects[2].printValues()
        objects[3].render()
        objects[3].printValues()
        vars["current_state"] = 7
    
    #need_matrix creation
    if (vars["current_state"] == 7):
        objects.append(objects[1] - objects[2])
        objects[4].is_renderable = True
        vars["resources"] = [Resource(vars["input_resources"].value, objects[0].vals[i], i) for i in range(vars["input_resources"].value)]
        vars["processes"] = [Process(vars["input_processes"].value, i) for i in range(vars["input_processes"].value)]
        vars["current_state"] = 8
    
    if (vars["current_state"] == 8):
        renderObjects(objects)
        fill(0)
        textSize(24)
        text("Press SPACE to begin", 600, 50)
        if key == " ":
            vars["current_state"] = 9
    
    #Using Bankers Algorithm
    if (vars["current_state"] == 9):
        renderObjects(objects)
        bankersAlgorithm(objects)
    
    #Show results    
    if (vars["current_state"] == 10):
        renderObjects(objects)
        textSize(20)
        if len(vars["safe_sequence"]) == vars["input_processes"].value:
            fill(0, 150, 0)
            text(vars["sequence_string"], 600, 100)
        else:
            fill(150, 0, 0)
            text("DEADLOCK", 600, 100)
        fill(0)
        textSize(24)
        text("Press ENTER to start again", 600, 50)
        if (key == ENTER or key == RETURN) and keyPressed:
            vars["current_state"] = 0
            global objects
            objects = []
            vars["counter"] = 0
            vars["time"] = 0
            vars["safe_sequence"] = []
            vars["sequence_string"] = ""
            vars["input_processes"].value = 1
            vars["input_resources"].value = 1
