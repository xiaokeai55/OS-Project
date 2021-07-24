from burst import*
from CPUburst import*
from FCFS import*
import sys
import math

#def next_exp():
    
class Rand48(object):
    def __init__(self, seed):
        self.n = seed

    def seed(self, seed):
        self.n = seed

    def srand(self, seed):
        self.n = (seed << 16) + 0x330e

    def next(self):
        self.n = (25214903917 * self.n + 11) & (2 ** 48 - 1)
        return self.n

    def drand(self):
        return self.next() / 2 ** 48

def next_exp(seed, Lambda, upper):
    rand = Rand48(seed)
    rand.srand(seed)
    while(True):
        r = rand.drand()
        x = -math.log(r)/Lambda
        if x <= upper:
            return x
    
        


# argv[1]: Define n as the number of processes to simulate
# argv[2]: seed for the random number generator
# argv[3]: parameter λ, 1/λ will be the average random value generated
# argv[4]: upper bound for valid pseudo-random numbers 
# argv[5]: Define t_cs as the time, in milliseconds, that it takes to perform a context switch. Expect tcs
#           to be a positive even integer.
# argv[6]: For the SJF and SRT algorithms, the constant α
# argv[7]: For the RR algorithm, define the time slice value, t_slice, measured in milliseconds
if __name__ == '__main__':
    processes = []
    
    if len(sys.argv) != 8:
        raise Exception("invalid args number")
    process_num = int(sys.argv[1])
    seed = int(sys.argv[2])
    Lambda = float(sys.argv[3])
    upper_bound = int(sys.argv[4])
    t_cs = int(sys.argv[5])
    alpha = float(sys.argv[6])
    t_slice = int(sys.argv[7])
    rand = Rand48(seed)
    rand.srand(seed)
    bursts = []
    for i in range(process_num):
        arrival = math.floor(next_exp(seed, Lambda, upper_bound))
        burst_num = math.ceil(rand.drand() * 100)
        print(burst_num)
        for j in range(burst_num - 1):
            bursts.append(CPUburst('CPU', math.ceil(next_exp(seed, Lambda, upper_bound))))
            bursts.append(CPUburst('IO', 10 * math.ceil(next_exp(seed, Lambda, upper_bound))))
        bursts.append(CPUburst('CPU', math.ceil(next_exp(seed, Lambda, upper_bound))))
        process = Burst(chr(65+i), arrival, burst_num, bursts)
        processes.append(process)
    
        
    #FCFS
    #fcfs = FCFS(processes[0], t_cs) 
    #fcfs.run()
    