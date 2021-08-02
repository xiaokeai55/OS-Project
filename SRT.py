from Process import*
from copy import deepcopy
import math

class SRT(object):


    def __init__(self, processes, t_cs, alpha, Lambda):

        #simout
        self.cpu_time = 0
        self.turnaround_time = 0
        self.wait_time = 0
        self.cs_num = 0
        self.preemp = 0
        self.cpu_utilization = 0

        ##########################

        self.process_num = len(processes)
        self.processes = sorted(deepcopy(processes))
        self.readyQ = []
        self.total = []
        self.Lambda = Lambda
        for i in range(0, self.process_num, 1):
            self.total.append(processes[i].getBurstNum())
            for j in range(0, processes[i].getBurstNum()*2, 2):
                self.cpu_time += processes[i].getBursts()[j]
        
        self.t_cs = t_cs//2
        self.alpha = alpha
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
        self.p = False



    def calc_predict(self,a, t ,tp):
        return math.ceil(a * t + (1 - a)* tp)



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
                self.readyQ = sorted(self.readyQ)
                print('time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]'
                    .format(self.processes[self.arrival_index].getArrival(), self.processes[self.arrival_index], self.processes[self.arrival_index].predictBursts(), self.checkQ()))
                self.wait_time = self.wait_time - self.processes[self.arrival_index].getArrival()
                self.processes[self.arrival_index].notfirst()
                self.arrival_index += 1
                
    def switch(self, count):
        tmp = self.current
        self.current = self.next_arr
        self.next_arr = tmp
        self.count = self.current.getCount()
        self.bursts = deepcopy(self.current.getBursts())
        ret = self.current.getCount()
        return ret
        
    def checkIO(self, count, time, cs):
        ret = count
        tmp = False
        tmp2 = False
        pmpt = None
        if cs:
            while len(self.nextblock) != 0 and time == self.nextblock[0].getArrival():
                self.checkArrival(self.nextblock[0].getArrival())
                tmp = True
                self.nextblock[0].count+=1
                self.readyQ.append(self.nextblock[0])
                self.readyQ = sorted(self.readyQ)
                print('time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]'
                    .format(self.nextblock[0].getArrival(), self.nextblock[0], self.nextblock[0].predictBursts(), self.checkQ()))
                self.wait_time = self.wait_time - self.nextblock[0].getArrival()
                self.nextblock.pop(0)
            if len(self.readyQ) != 0:
                tmp2 = True
                tmp_burst = self.readyQ.pop(0)
                time += self.t_cs
        pre = False
        for i in range(len(self.nextblock)):
            
            if len(self.nextblock) != 0 and time > self.nextblock[0].getArrival():
                self.p = True
                self.checkArrival(self.nextblock[0].getArrival())
                if not self.r and (not tmp): 
                    if self.nextblock[0].getName() == self.current.getName(): ret += 1

                    self.time = self.nextblock[0].getArrival()
                    tmp = True
                
                tP = False
                if not pre:
                    spend = self.nextblock[0].getArrival() - self.current.getStartTime()
                else:
                    spend = self.nextblock[0].getArrival() - self.current.getStartTime() - self.t_cs
                self.current.setStartTime(self.nextblock[0].getArrival())

                self.current.setRemaining(self.current.getRem() - spend)
                switch = self.nextblock[0]
                if self.nextblock[0].getRem() < self.current.getRem():
                    tP = True
                    self.current.setSpending(self.current.predictBursts()-self.current.getRem())
                    switch = self.current
                    self.current = self.nextblock[0]
                    self.current.setStartTime(self.nextblock[0].getArrival())

                self.nextblock[0].count+=1
                self.readyQ.append(self.nextblock[0])
                for x in range(len(self.readyQ)):
                    self.readyQ[x].setCompareProcess(self.readyQ[x].getC3())
                self.readyQ = sorted(self.readyQ)
                if tP and not pre:
                    pre = True
                    pmpt = self.nextblock[0]
                    self.time = self.nextblock[0].getArrival() + self.t_cs
                    print('time {}ms: Process {} (tau {}ms) completed I/O; preempting {} [Q {}]'
                        .format(self.nextblock[0].getArrival(), self.nextblock[0],self.nextblock[0].predictBursts(), switch, self.checkQ()))
                    self.wait_time = self.wait_time - self.nextblock[0].getArrival()
                    self.preemp+=1
                    self.readyQ.append(switch)
                    self.readyQ = sorted(self.readyQ)
                    self.time+=self.t_cs 

                    if len(self.nextblock) > 1:
                        if self.nextblock[1].getArrival() > self.time:
                            self.nextblock.pop(0)
                            break
                else:
                    print('time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]'
                    .format(self.nextblock[0].getArrival(), self.nextblock[0],self.nextblock[0].predictBursts(), self.checkQ()))
                    self.wait_time = self.wait_time - self.nextblock[0].getArrival()
                self.nextblock.pop(0)
                i-=1
        if pmpt != None:
            self.readyQ.pop(0)
        if tmp:
            self.time += self.t_cs
        if tmp2:
            self.readyQ = sorted(self.readyQ)
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

        #set each process compare method to SRT_compare
        for i in range(self.process_num):
            self.processes[i].setPredictBursts(int(1/self.Lambda))
            self.processes[i].setRemaining(int(1/self.Lambda))
            self.processes[i].setCompareProcess(self.processes[i].getC3())

        
        self.current = self.processes[0]
        if self.process_num > 1:
            self.next_arr = self.processes[1]
        else:
            self.next_arr = self.processes[0]


        print('time {}ms: Simulator started for SRT [Q {}]'.format(self.time, self.checkQ()))
        self.time = self.processes[0].getArrival()
        self.readyQ.append(self.processes[0])
        self.readyQ = sorted(self.readyQ)
        self.current = self.readyQ[0]

        print('time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]'
            .format(self.time, self.current, self.current.predictBursts(),self.checkQ()))
        self.wait_time = self.wait_time - self.time
        self.current.notfirst()
        i = 0
        while 1:
            i = self.checkIO(i, self.time, False)
            self.checkArrival(self.time)
            if(len(self.readyQ) == 0):
                self.time = self.nextblock[0].getArrival()
                i = self.switch(i)
                i = self.checkIO(i, self.time, True)
                i = self.switch(i)
                self.current = self.readyQ[0]
                i = self.readyQ[0].getCount()
                self.bursts = self.readyQ[0].getBursts()
                self.readyQ.pop(0)
            else:
                i = self.cs(i, True)
                self.current = self.readyQ[0]
                i = self.readyQ[0].getCount()
                self.bursts = self.readyQ[0].getBursts()
                self.readyQ.pop(0)
                self.current.setStartTime(self.time)
            while 1:
                self.wait_time = self.wait_time + self.time - self.t_cs
                self.cs_num+=1
                if(self.current.getSpending() == 0):
                    print('time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]'\
                        .format(self.time, self.current, self.current.predictBursts(), self.bursts[i], self.checkQ()))
                else:
                    print('time {}ms: Process {} (tau {}ms) started using the CPU for remaining {}ms of {}ms burst [Q {}]'\
                        .format(self.time, self.current, self.current.predictBursts(), 
                                self.bursts[i]-self.current.getSpending(), self.bursts[i], self.checkQ()))


                self.r = True
                self.current.setStartTime(self.time)
                if len(self.readyQ) != 0 and self.readyQ[0].getRem() < self.current.getRem():
                    print('time {}ms: Process {} (tau {}ms) will preempt {} [Q {}]'.format(self.time, self.readyQ[0], self.readyQ[0].predictBursts(), 
                                self.current, self.checkQ()))
                    self.wait_time = self.wait_time - self.time - self.t_cs
                    self.preemp+=1
                    self.readyQ.append(self.current)
                    self.current = self.readyQ.pop(0)
                    self.readyQ = sorted(self.readyQ)
                    self.bursts = self.current.getBursts()
                    i = self.current.getCount()
                    self.time+=self.t_cs*2
                    continue
                break
            self.checkArrival(self.time + self.t_cs)
            ###
            tCurrent = self.current 
            while len(self.nextblock) > 0:
                u = self.current.getCount()
                b = self.current.getBursts()
                self.p = False
                if self.nextblock[0].getArrival() < self.time + self.t_cs + b[u] - self.current.getSpending():
                    i = self.checkIO(i, self.time + self.bursts[i] -self.current.getSpending(), False)
                    #print(self.current)
                    #print(tCurrent)
                    if self.current != tCurrent:
                        i = self.current.getCount()
                        self.bursts = self.current.getBursts()
                        self.current.setStartTime(self.time)
                        tCurrent = self.current 
                        self.cs_num+=1
                        if(self.current.getSpending() == 0):
                            print('time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]'\
                                .format(self.time, self.current, self.current.predictBursts(), self.bursts[i], self.checkQ()))
                        else:
                            print('time {}ms: Process {} (tau {}ms) started using the CPU for remaining {}ms of {}ms burst [Q {}]'\
                                .format(self.time, self.current, self.current.predictBursts(), 
                                        self.bursts[i]-self.current.getSpending(), self.bursts[i], self.checkQ()))
                        if not self.p:
                            break
                    else:
                        break
                else:
                    break
            
            self.checkArrival(self.time + self.t_cs)
            self.time += self.bursts[i] - self.current.getSpending()
            

            self.total[ord(self.current.getName())-65]-=1
            self.checkArrival(self.time)
            if self.total[ord(self.current.getName())-65] == 1:
                
                print('time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]'
                    .format(self.time, self.current, self.current.predictBursts(), self.total[ord(self.current.getName())-65], self.checkQ()))
                rec = self.calc_predict(self.alpha, self.bursts[i], self.current.predictBursts())
                print('time {}ms: Recalculated tau from {}ms to {}ms for process {} [Q {}]'
                    .format(self.time, self.current.predictBursts(), rec, self.current, self.checkQ()))
                self.current.setSpending(0)
                self.current.setPredictBursts(rec)
                self.current.setRemaining(rec)
                
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
            else: 
                print('time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]'.format(self.time, self.current, self.current.predictBursts(),self.total[ord(self.current.getName())-65], self.checkQ()))
                rec = self.calc_predict(self.alpha, self.bursts[i], self.current.predictBursts())
                print('time {}ms: Recalculated tau from {}ms to {}ms for process {} [Q {}]'
                    .format(self.time, self.current.predictBursts(), rec, self.current, self.checkQ()))
                self.current.setSpending(0)
                self.current.setPredictBursts(rec)
                self.current.setRemaining(rec)

            self.r = False
            i += 1
            self.current.setCount(i)
            
            block = self.time + self.bursts[i] + self.t_cs
            self.current.update_arrival(block)
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]'.format(self.time, self.current, block, self.checkQ()))
            self.nextblock.append(self.current)
            for n in self.nextblock:
                n.setCompareProcess(n.getC1())
            self.nextblock.sort()
            for n in self.nextblock:
                n.setCompareProcess(n.getC2())

            self.checkArrival(self.time)
            if self.next_arr != -1:
                if self.next_arr.getName() != self.nextblock[0].getName():
                    if self.next_arr.getArrival() > self.nextblock[0].getArrival():
                        self.next_arr = self.nextblock[0]
                    i = self.switch(i)
                    i = self.cs(i, False)
                else:
                    i = self.switch(i)
                    i = self.cs(i, False)
        i = self.cs(i, False)
        print('time {}ms: Simulator ended for SRT [Q {}]'.format(self.time, self.checkQ()))
        self.cpu_utilization = self.cpu_time/self.time*100
        self.turnaround_time = self.wait_time+self.cpu_time+self.t_cs*self.cs_num*2
        
    def getcpu(self):
        return self.cpu_time/(self.cs_num-self.preemp)
    
    def getturn(self):
        return self.turnaround_time/(self.cs_num-self.preemp)
    
    def getwait(self):
        return self.wait_time/(self.cs_num-self.preemp)
    
    def getcs(self):
        return self.cs_num
    
    def getpreemp(self):
        return self.preemp
    
    def getutilization(self):
        return self.cpu_utilization