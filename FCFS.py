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
        self.bursts = deepcopy(self.processes[0].getBursts())
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
        self.nextblock = []
        self.r = False
        self.stop = 0
    
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
        if self.next_arr != -1 and self.next_arr.getArrival() < time and self.next_arr.isfirst():
            self.readyQ.append(self.next_arr)
            print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(self.next_arr.getArrival(), self.next_arr, self.checkQ()))
            self.next_arr.notfirst()
                
    def switch(self, count):
        self.current.setCount(count)
        #print('switch', self.current, self.current.getCount())
        #print(self.next_arr, self.next_arr.getCount())
        tmp = self.current
        self.current = self.next_arr
        self.next_arr = tmp
        self.count = self.current.getCount()
        self.bursts = deepcopy(self.current.getBursts())
        ret = self.current.getCount()
        return ret
        
    def checkIO(self, count, time):
        #print('checkIO', self.current)
        #print(self.next_arr)
        ret = count
        if len(self.nextblock) != 0 and time >= self.nextblock[0].getArrival():
            if not self.r: 
                self.time = self.nextblock[0].getArrival()
                self.time += self.t_cs
            self.readyQ.append(self.next_arr)
            print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(self.next_arr.getArrival(), self.next_arr, self.checkQ()))
            self.nextblock.pop(0)
            self.next_arr.setCount(self.next_arr.getCount()+1)
            if self.next_arr.getName() == self.current.getName(): ret += 1
        return ret
    
    def run(self):
        print('time {}ms: Simulator started for FCFS [Q {}]'.format(self.time, self.checkQ()))
        self.time = self.processes[0].getArrival()
        self.readyQ.append(self.processes[0])
        self.current = self.readyQ[0]
        print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(self.time, self.current, self.checkQ()))
        self.current.notfirst()
        i = 0
        while 1:
            self.time += self.t_cs
            self.checkArrival(self.time)
            i = self.checkIO(i, self.time)
            if(len(self.readyQ) == 0):
                self.time = self.nextblock[0].getArrival()
                i = self.switch(i)
                i = self.checkIO(i, self.time)
                i = self.switch(i)
            self.readyQ.pop(0)
            print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'\
                  .format(self.time, self.current, self.bursts[i], self.checkQ()))
            self.r = True
            self.cpu_time += self.bursts[i]
            self.checkArrival(self.time + self.t_cs)
            i = self.checkIO(i, self.time + self.bursts[i])
            self.time += self.bursts[i]
            self.total[ord(self.current.getName())-65]-=1
            self.checkArrival(self.time + self.t_cs)
            if self.total[ord(self.current.getName())-65] == 1: print('time {}ms: Process {} completed a CPU burst; {} burst to go [Q {}]'.format(self.time, self.current, self.total[ord(self.current.getName())-65], self.checkQ()))
            elif self.total[ord(self.current.getName())-65] == 0: 
                print('time {}ms: Process {} terminated [Q {}]'.format(self.time, self.current, self.checkQ()))
                self.stop+=1
                if self.stop == self.process_num: break
                self.current = self.next_arr
                i = self.current.getCount()
                self.bursts = deepcopy(self.current.getBursts())
                self.r = False
                continue
            else: print('time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]'.format(self.time, self.current, self.total[ord(self.current.getName())-65], self.checkQ()))
            self.r = False
            i += 1
            block = self.time + self.bursts[i] + self.t_cs
            self.wait_time += self.bursts[i]
            self.current.update_arrival(block)
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]'.format(self.time, self.current, block, self.checkQ()))
            #print(self.current.getName(),self.current.getArrival())
            self.nextblock.append(self.current)
            self.nextblock.sort()
            self.checkArrival(block)
            #print('nextblock'+self.nextblock[0].getName())
            #print('nextarr'+self.next_arr.getName())
            if self.next_arr != -1:
                if self.next_arr.getName() != self.nextblock[0].getName():
                    if self.next_arr.getArrival() > self.nextblock[0].getArrival():
                        self.next_arr = self.nextblock[0]
                    i = self.switch(i)
                    self.time += self.t_cs
                    continue
                else:
                    i = self.switch(i)
            self.time = self.current.getArrival()
            #print('aaaaaa')
            self.readyQ.append(self.processes[ord(self.current.getName())-65])
            print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(self.time, self.current, self.checkQ()))
            self.nextblock.pop(0)
            self.current = self.readyQ[0]
            i += 1
            self.current.setCount(i)
        self.time += self.t_cs
        print('time {}ms: Simulator ended for FCFS [Q {}]'.format(self.time, self.checkQ()))
        self.cpu_utilization = self.cpu_time/self.time*100
        
    def getcpu(self):
        return self.cpu_time/self.processes[ord(self.current.getName())-65].getBurstNum()
    
    def getturn(self):
        return self.turnaround_time/self.processes[ord(self.current.getName())-65].getBurstNum()
    
    def getwait(self):
        return self.wait_time/self.processes[ord(self.current.getName())-65].getBurstNum()
    
    def getcs(self):
        return self.cs_num
    
    def getpreemp(self):
        return self.preemp
    
    def getutilization(self):
        return self.cpu_utilization
    