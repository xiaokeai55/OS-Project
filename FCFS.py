from Process import*
from copy import deepcopy
class FCFS(object):
    def __init__(self, processes, t_cs):
        self.process_num = len(processes)
        self.total = []
        for i in range(self.process_num):
            self.total.append(processes[i].getBurstNum())
        self.processes = sorted(deepcopy(processes))
        self.readyQ = []
        self.t_cs = t_cs//2
        self.time = 0
        self.index = 0
        self.current = self.processes[0]
        self.bursts = deepcopy(self.processes[0].getBursts())
        if self.process_num > 1:
            self.next_arr = self.processes[1]
        else:
            self.next_arr = self.processes[0]
        self.nextblock = []
        self.r = False
        self.stop = 0
        self.arrival_index = 1
        #print(self.processes[0])
        #print(self.processes[0].getBursts())
        
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
            ret = ''
            for i in self.readyQ:
                ret += i.getName()
            return ret
        
    def checkArrival(self, time):
        for _ in range(self.process_num):
            if self.arrival_index < self.process_num and self.processes[self.arrival_index].getArrival() < time and self.processes[self.arrival_index].isfirst():
                self.readyQ.append(self.processes[self.arrival_index])
                print('time {}ms: Process {} arrived; added to ready queue [Q {}]'.format(self.processes[self.arrival_index].getArrival(), self.processes[self.arrival_index], self.checkQ()))
                self.processes[self.arrival_index].notfirst()
                self.arrival_index += 1
                
    def switch(self, count):
        #self.current.setCount(count)
        #print('switch', self.current, self.current.getCount())
        #print(self.next_arr, self.next_arr.getCount())
        tmp = self.current
        self.current = self.next_arr
        self.next_arr = tmp
        self.count = self.current.getCount()
        self.bursts = deepcopy(self.current.getBursts())
        ret = self.current.getCount()
        return ret
        
    def checkIO(self, count, time, cs):
        #print(self.current)
        #print('checkIO', self.current)
        #print(self.next_arr)
        ret = count
        tmp = False
        tmp2 = False
        if cs:
            while len(self.nextblock) != 0 and time == self.nextblock[0].getArrival():
                self.checkArrival(self.nextblock[0].getArrival())
                tmp = True
                self.nextblock[0].count+=1
                self.readyQ.append(self.nextblock[0])
                print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(self.nextblock[0].getArrival(), self.nextblock[0], self.checkQ()))
                self.nextblock.pop(0)
            if len(self.readyQ) != 0:
                tmp2 = True
                tmp_burst = self.readyQ.pop(0)
            time+=self.t_cs
        for i in range(len(self.nextblock)):
            if len(self.nextblock) != 0 and time > self.nextblock[0].getArrival():
                self.checkArrival(self.nextblock[0].getArrival())
                if not self.r and (not tmp): 
                    if self.nextblock[0].getName() == self.current.getName(): ret += 1
                    self.time = self.nextblock[0].getArrival()
                    tmp = True
                self.nextblock[0].count+=1
                self.readyQ.append(self.nextblock[0])
                print('time {}ms: Process {} completed I/O; added to ready queue [Q {}]'.format(self.nextblock[0].getArrival(), self.nextblock[0], self.checkQ()))
                self.nextblock.pop(0)
                i-=1
        if tmp:
            self.time += self.t_cs
        if tmp2:
            self.readyQ.insert(0, tmp_burst)
        return ret

    def cs(self, count, s):
        tmp = self.time
        if s:
            ret = self.checkIO(count, self.time, s)
        else:
            ret = self.checkIO(count, self.time+self.t_cs, s)
        self.time = tmp+self.t_cs
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
            i = self.checkIO(i, self.time, False)
            self.checkArrival(self.time)
            if len(self.readyQ) == 0:
                self.time = self.nextblock[0].getArrival()
                #print(self.nextblock[0])
                #print(self.next_arr)
                i = self.switch(i)
                i = self.checkIO(i, self.time, True)
                i = self.switch(i)
                self.current = self.readyQ[0]
                i = self.readyQ[0].getCount()
                self.bursts = self.readyQ[0].getBursts()
                self.readyQ.pop(0)
            else:
                self.current = self.readyQ[0]
                i = self.readyQ[0].getCount()
                self.bursts = self.readyQ[0].getBursts()
                i = self.cs(i, True)
                self.readyQ.pop(0)
            print('time {}ms: Process {} started using the CPU for {}ms burst [Q {}]'\
                  .format(self.time, self.current, self.bursts[i], self.checkQ()))
            self.r = True
            self.cpu_time += self.bursts[i]
            self.checkArrival(self.time + self.t_cs)
            i = self.checkIO(i, self.time + self.bursts[i], False)
            self.time += self.bursts[i]
            self.total[ord(self.current.getName())-65]-=1
            self.checkArrival(self.time)
            if self.total[ord(self.current.getName())-65] == 1: print('time {}ms: Process {} completed a CPU burst; {} burst to go [Q {}]'.format(self.time, self.current, self.total[ord(self.current.getName())-65], self.checkQ()))
            elif self.total[ord(self.current.getName())-65] == 0: 
                print('time {}ms: Process {} terminated [Q {}]'.format(self.time, self.current, self.checkQ()))
                self.stop+=1
                if self.stop == self.process_num: break
                self.current = self.next_arr
                i = self.current.getCount()
                self.bursts = deepcopy(self.current.getBursts())
                self.r = False
                i = self.cs(i, False)
                continue
            else: print('time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]'.format(self.time, self.current, self.total[ord(self.current.getName())-65], self.checkQ()))
            self.r = False
            i += 1
            self.current.setCount(i)
            block = self.time + self.bursts[i] + self.t_cs
            self.current.update_arrival(block)
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]'.format(self.time, self.current, block, self.checkQ()))
            #print(self.current.getName(),self.current.getArrival())
            self.nextblock.append(self.current)
            self.nextblock.sort()
            #print(self.nextblock[0])
            self.checkArrival(self.time)
            #print('nextblock'+self.nextblock[0].getName())
            #print('nextarr'+self.next_arr.getName())
            if self.next_arr != -1:
                if self.next_arr.getName() != self.nextblock[0].getName():
                    if self.next_arr.getArrival() > self.nextblock[0].getArrival():
                        self.next_arr = self.nextblock[0]
                    i = self.switch(i)
                    i = self.cs(i, False)
                elif len(self.readyQ) != 0:
                    i = self.cs(i, False)
                else:
                    i = self.switch(i)
        i = self.cs(i, False)
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
    