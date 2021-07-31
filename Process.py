class Process(object):
    def __init__(self, ID, arrival, cpu, bursts):
        self.id = ID
        self.arrival = arrival
        self.cpu = cpu
        self.bursts = bursts
        self.preemp = False
        self.count = 0
        self.first = True
        self.remaining = None

        self.predict_bursts = None
        def SJF_compare(self,p2):
            if self.predict_bursts == p2.predictBursts():
                return self.id < p2.getName()
            return self.predict_bursts < p2.predictBursts()
        def FCFS_compare(self,p):
            if self.arrival == p.getArrival():
                return self.id < p.getName()
            return self.arrival < p.getArrival()

        def SRT_compare(self,p):
            if self.remaining == p.getRem():
                return self.id < p.getName()
            return self.remaining < p.getRem()
            
        self.compare2 = SJF_compare
        self.compare1 = FCFS_compare
        self.compare3 = SRT_compare
        self.compare_process = FCFS_compare
    
    def getC2(self):
        return self.compare2

    def getC3(self):
        return self.compare3

    def getC1(self):
        return self.compare1
    
    def getRem(self):
        return self.remaining

    def setCompareProcess(self, c):
        self.compare_process = c

    def setPredictBursts(self,c):
        self.predict_bursts = c

    def predictBursts(self):
        return self.predict_bursts
    
    def getName(self):
        return self.id
    
    def getBurstNum(self):
        return self.cpu
    
    def getBursts(self):
        return self.bursts
    
    def getArrival(self):
        return self.arrival

    def __lt__(self, p):
        return self.compare_process(self, p)
    
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