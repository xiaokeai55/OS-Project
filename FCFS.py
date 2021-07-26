from burst import*
from copy import deepcopy
class FCFS(object):
    def __init__(self, processes, t_cs):
        self.processes = deepcopy(processes)
        self.readyQ = []
        self.total = 0
        self.t_cs = t_cs//2
        self.current = 0
        #simout
        self.cpu_time = 0
        self.turnaround_time = 0
        self.wait_time = 0
        self.cs_num = 0
        self.preemp = 0
        self.cpu_utilization = 0
    
    def checkQ(self):
        if len(self.readyQ) == 0:
            return 'empty'
        else:
            s = ''
            for i in self.readyQ:
                s += i
            ret = ' '
            ret = ret.join(s)
            return ret
        
    def run(self):
        time = 0
        print('time {}ms: Simulator started for FCFS [Q {}]'.format(time, self.checkQ()))
        time = self.processes[self.current].getArrival()
        bursts = self.processes[self.current].getBursts()
        self.total = self.processes[self.current].getBurstNum()
        self.readyQ.append(self.processes[self.current].getName())
        current = self.readyQ[0]
        print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(time, current, self.checkQ()))
        self.readyQ.pop(0)
        for i in range(0, len(bursts) - 1, 2):
            time += self.t_cs
            print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'.format(time, current, bursts[i].getTime(), self.checkQ()))
            self.cpu_time += bursts[i].getTime()
            time += bursts[i].getTime()
            self.total-=1
            if self.total == 1: print('time {}ms: Process {} completed a CPU burst; {} burst to go [Q {}]'.format(time, current, self.total, self.checkQ()))
            else: print('time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]'.format(time, current, self.total, self.checkQ()))
            block = time + bursts[i+1].getTime() + self.t_cs
            self.wait_time += bursts[i+1].getTime()
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]'.format(time, current, block, self.checkQ()))
            time = block
            self.readyQ.append(self.processes[self.current].getName())
            print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(time, current, self.checkQ()))
            current = self.readyQ[0]
            self.readyQ.pop(0)
        time += self.t_cs
        print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'.format(time, current, bursts[-1].getTime(), self.checkQ()))
        time += bursts[-1].getTime()
        self.cpu_time += bursts[-1].getTime()
        self.turnaround_time = self.cpu_time + self.wait_time
        self.total-=1
        print('time {}ms: Process {} terminated [Q {}]'.format(time, current, self.checkQ()))
        time += self.t_cs
        print('time {}ms: Simulator ended for FCFS [Q {}]'.format(time, self.checkQ()))
        self.cpu_utilization = self.cpu_time/time*100
        
    def getcpu(self):
        return self.cpu_time/self.processes[self.current].getBurstNum()
    
    def getturn(self):
        return self.turnaround_time/self.processes[self.current].getBurstNum()
    
    def getwait(self):
        return self.wait_time/self.processes[self.current].getBurstNum()
    
    def getcs(self):
        return self.cs_num
    
    def getpreemp(self):
        return self.preemp
    
    def getutilization(self):
        return self.cpu_utilization
    