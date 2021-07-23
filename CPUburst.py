class CPUburst:
    def __init__(self, CPU, time):
        if(CPU == 'CPU'):
            self.CPU = True #CPU burst
        else: self.CPU = False #IO burst
        self.time = time