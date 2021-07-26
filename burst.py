class Burst(object):
    def __init__(self, ID, arrival, cpu, bursts):
        self.id = ID
        self.arrival = arrival
        self.cpu = cpu
        self.bursts = bursts
    
    def getName(self):
        return self.id
    
    def getBurstNum(self):
        return self.cpu
    
    def getBursts(self):
        return self.bursts
    
    def getArrival(self):
        return self.arrival
        