from Process import*
from copy import deepcopy
class FCFS(object):
    def __init__(self, processes, t_cs):
        self.processes = sorted(deepcopy(processes))
        self.process_num = len(processes)
        self.readyQ = []
        self.total = []
        for i in range(self.process_num):
            self.processes[i].setindex(i)
            self.total.append(self.processes[i].getBurstNum())
        self.t_cs = t_cs//2
        self.time = 0
        self.index = 0
        self.current = self.processes[0]
        self.bursts = self.processes[0].getBursts()
        if self.process_num > 1:
            self.next_arr = self.processes[1]
        else:
            self.next_arr = -1
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
                s += i.getName()
            ret = ' '
            ret = ret.join(s)
            return ret
        
    def checkArrival(self, time):
        if self.next_arr != -1 and self.next_arr.isfirst() and self.next_arr.getArrival() < time:
            self.readyQ.append(self.next_arr)
            print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(self.next_arr.getArrival(), self.next_arr, self.checkQ()))
            self.next_arr.notfirst()
                
    def switch(self, count):
        self.current.setCount(count)
        self.current, self.next_arr = self.next_arr, self.current
        self.index = self.current.getindex()
        self.bursts = self.current.getBursts()
        i = self.current.getCount()
        return i
        
    def run(self):
        print('time {}ms: Simulator started for FCFS [Q {}]'.format(self.time, self.checkQ()))
        self.time = self.processes[0].getArrival()
        self.readyQ.append(self.processes[0])
        self.current = self.readyQ[0]
        print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(self.time, self.current, self.checkQ()))
        self.readyQ.pop(0)
        i = 0
        while i < len(self.bursts) - 1:
            self.time += self.t_cs
            self.checkArrival(self.time)
            print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'.format(self.time, self.current, self.bursts[i], self.checkQ()))
            self.cpu_time += self.bursts[i]
            self.checkArrival(self.time + self.t_cs)
            self.time += self.bursts[i]
            self.total[self.index]-=1
            self.checkArrival(self.time + self.t_cs)
            if self.total[self.index] == 1: print('time {}ms: Process {} completed a CPU burst; {} burst to go [Q {}]'.format(self.time, self.current, self.total[self.index], self.checkQ()))
            else: print('time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]'.format(self.time, self.current, self.total[self.index], self.checkQ()))
            i += 1
            block = self.time + self.bursts[i] + self.t_cs
            self.wait_time += self.bursts[i]
            self.current.update_arrival(block)
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]'.format(self.time, self.current, block, self.checkQ()))
            self.checkArrival(block)
            if self.checkQ != 'empty':
                i = self.switch(i)
                self.time += self.t_cs
                continue
            self.time = block
            self.readyQ.append(self.processes[self.index])
            print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(self.time, self.current, self.checkQ()))
            self.current = self.readyQ[0]
            self.readyQ.pop(0)
            i += 1
            self.current.setCount = i
        self.time += self.t_cs
        self.checkArrival(self.time)
        print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'.format(self.time, self.current, self.bursts[-1], self.checkQ()))
        self.time += self.bursts[-1]
        self.cpu_time += self.bursts[-1]
        self.turnaround_time = self.cpu_time + self.wait_time
        self.total[self.index]-=1
        self.checkArrival(self.time)
        print('time {}ms: Process {} terminated [Q {}]'.format(self.time, self.current, self.checkQ()))
        self.time += self.t_cs
        print('time {}ms: Simulator ended for FCFS [Q {}]'.format(self.time, self.checkQ()))
        self.cpu_utilization = self.cpu_time/self.time*100
        
    def getcpu(self):
        return self.cpu_time/self.processes[self.index].getBurstNum()
    
    def getturn(self):
        return self.turnaround_time/self.processes[self.index].getBurstNum()
    
    def getwait(self):
        return self.wait_time/self.processes[self.index].getBurstNum()
    
    def getcs(self):
        return self.cs_num
    
    def getpreemp(self):
        return self.preemp
    
    def getutilization(self):
        return self.cpu_utilization
    