from burst import*
class FCFS(object):
    def __init__(self, processes, t_cs):
        self.processes = processes
        self.readyQ = []
        self.total = 0
        self.t_cs = t_cs
    
    def checkQ(self):
        if len(self.readyQ) == 0:
            return ' empty'
        else:
            ret = ''
            for i in self.readyQ:
                ret += ' '
                ret += i
            return ret
        
    def run(self):
        time = 0
        print('time {}ms: Simulator started for FCFS [Q{}]'.format(time, self.checkQ()))
        time = self.processes.getArrival()
        bursts = self.processes.getBursts()
        self.total = len(bursts) // 2
        self.readyQ.append(self.processes.getName())
        current = self.readyQ[0]
        print('time {}ms: Process {} arrived; added to ready queue [Q{}]'.format(time, current, self.checkQ()))
        self.readyQ.pop(0)
        for i in range(len(bursts) // 2):
            time += self.t_cs
            print('time {}ms: Process {} started using the CPU for {}ms burst [Q{}]'.format(time, current, bursts[0].getTime(), self.checkQ()))
            time += bursts[i].getTime()
            self.total-=1
            print('time {}ms: Process {} completed a CPU burst; {} bursts to go [Q{}]'.format(time, current, self.total, self.checkQ()))
            print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q{}]'.format(time, current, bursts[i].getTime(), self.checkQ()))
            self.readyQ.append(self.processes.getName())
            print('time {}ms: Process {} completed I/O; added to ready queue [Q{}]'.format(time, current, self.checkQ()))
            current = self.readyQ[0]
            self.readyQ.pop(0)
        time += self.t_cs
        print('time {}ms: Process {} started using the CPU for {}ms burst [Q{}]'.format(time, current, bursts[0].getTime(), self.checkQ()))
        time += bursts[-1].getTime()
        self.total-=1
        print('time {}ms: Process {} terminated [Q{}]'.format(time, current, self.checkQ()))
        time += self.t_cs
        print('time {}ms: Simulator ended for FCFS [Q{}]'.format(time, self.checkQ()))
    