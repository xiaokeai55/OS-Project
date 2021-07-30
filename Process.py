class Process(object):
    def __init__(self, ID, arrival, cpu, bursts):
        self.id = ID
        self.arrival = arrival
        self.cpu = cpu
        self.bursts = bursts
        self.preemp = False
        self.count = 0
        self.first = True
    
    def getName(self):
        return self.id
    
    def getBurstNum(self):
        return self.cpu
    
    def getBursts(self):
        return self.bursts
    
    def getArrival(self):
        return self.arrival
    
    def __lt__(self, p):
        return self.arrival < p.getArrival()
    
    def __str__(self):
        return self.id
    
    def update_arrival(self, time):
        self.arrival = time
    
    def setCount(self, i):
        self.count = i
        
    def getCount(self):
        return self.count
    
    def isfirst(self):
        return self.first
    
    def notfirst(self):
        self.first = False