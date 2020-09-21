import numpy as np
import matplotlib.pyplot as plt


class sysinfo:
    def __init__(self,):
        self.lines = []
        self.cpu_core_count = 0
        self.previdle = 0
        self.previowait = 0
        self.read_file('stat')
        self.count_cpu_cores()
        self.user = np.zeros([self.cpu_core_count+1, 2])
        self.nice = np.zeros([self.cpu_core_count+1, 2])
        self.system = np.zeros([self.cpu_core_count+1, 2])
        self.idle = np.zeros([self.cpu_core_count+1, 2])
        self.iowait = np.zeros([self.cpu_core_count+1, 2])
        self.irq = np.zeros([self.cpu_core_count+1, 2])
        self.softirq = np.zeros([self.cpu_core_count+1, 2])
        self.steal = np.zeros([self.cpu_core_count+1, 2])
        self.guest = np.zeros([self.cpu_core_count+1, 2])
        self.guest_nice = np.zeros([self.cpu_core_count+1, 2])
        self.cpu_load = 0

    def read_file(self, type):
        with open('/proc/' + type, 'r') as reader:
            file = reader.read()
        self.lines = file.splitlines()

    def count_cpu_cores(self,):
        self.cpu_core_count = 0
        for line in self.lines:
            if "cpu" in line:
                self.cpu_core_count += 1
        self.cpu_core_count -= 1

    def parse_stat(self,):
        self.user = np.roll(self.user, 1)
        self.nice = np.roll(self.nice, 1)
        self.system = np.roll(self.system, 1)
        self.idle = np.roll(self.idle, 1)
        self.iowait = np.roll(self.iowait, 1)
        self.irq = np.roll(self.irq, 1)
        self.softirq = np.roll(self.softirq, 1)
        self.steal = np.roll(self.steal, 1)
        self.guest = np.roll(self.guest, 1)
        self.guest_nice = np.roll(self.guest_nice, 1)
        for cpu in range(0, self.cpu_core_count+1):
            cur_data = self.lines[cpu].split()
            self.user[cpu, 0] = int(cur_data[1])
            self.nice[cpu, 0] = int(cur_data[2])
            self.system[cpu, 0] = int(cur_data[3])
            self.idle[cpu, 0] = int(cur_data[4])
            self.iowait[cpu, 0] = int(cur_data[5])
            self.irq[cpu, 0] = int(cur_data[6])
            self.softirq[cpu, 0] = int(cur_data[7])
            self.steal[cpu, 0] = int(cur_data[8])
            self.guest[cpu, 0] = int(cur_data[9])
            self.guest_nice[cpu, 0] = int(cur_data[10])

    def process_stat(self,):
        PrevIdle = self.idle[:, 1] + self.iowait[:, 1]
        Idle = self.idle[:, 0] + self.iowait[:, 0]
        PrevNonIdle = (self.user[:, 1] +
                       self.nice[:, 1] +
                       self.system[:, 1] +
                       self.irq[:, 1] +
                       self.softirq[:, 1] +
                       self.steal[:, 1])
        NonIdle = (self.user[:, 0] +
                   self.nice[:, 0] +
                   self.system[:, 0] +
                   self.irq[:, 0] +
                   self.softirq[:, 0] +
                   self.steal[:, 0])
        PrevTotal = PrevIdle + PrevNonIdle
        Total = Idle + NonIdle
        totald = Total - PrevTotal
        idled = Idle - PrevIdle
        self.cpu_load = (totald - idled)/totald

    def refresh_stat(self,):
        self.read_file('stat')
        self.parse_stat()
        self.process_stat()
        return self.cpu_load


# s = sysinfo()
# print(s.cpu_core_count)
# print(s.refresh_stat())
#
# dat = s.refresh_stat()[0]
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# Ln, = ax.plot(dat)
# ax.set_xlim([0, 100])
# ax.set_ylim([0, 1])
# plt.ion()
# plt.show()
# while True:
#     dat = np.append(dat, s.refresh_stat()[0])
#     Ln.set_ydata(dat)
#     Ln.set_xdata(range(len(dat)))
#     plt.pause(0.5)
