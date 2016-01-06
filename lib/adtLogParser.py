import numpy
import pickle
from connection import *


class Parser:
    def __init__(self, log_directory, device, build):
        self.log_directory = log_directory
        self.device = device
        self.build = build

    def collect_report(self):
        report_filename = self.log_directory + "/" + Config().reportFilename
        obj = [self.device, self.build, self.mem_log_parser(), self.cpu_log_parser(),  self.bty_usage_log_parser(),
               self.bty_temp_log_parser(), self.data_log_parser(), self.events_parser()]
        output = open(report_filename, 'wb')
        pickle.dump(obj, output, 2)

    def mem_log_parser(self):
        mem_filename = self.log_directory + "/" + Config().memFilename
        infile = open(mem_filename).readlines()
        num_lines = len(infile)
        mem_list = []
        time_list = []
        i = 0
        while i < num_lines:
            i += 1
            mem = 0
            mem_time = 0
            while i < num_lines and '---' not in infile[i]:
                if 'MemFree:' in infile[i]:
                    mem = int(infile[i].split()[-2])/1024
                if 'Time pass:' in infile[i]:
                    mem_time = int(infile[i].split()[-2])
                i += 1
            mem_list.append(mem)
            time_list.append(mem_time)
        report = [mem_list, time_list, max(mem_list), min(mem_list), numpy.average(mem_list)]

        return report

    def cpu_log_parser(self):
        cpu_filename = self.log_directory + "/" + Config().cpuFilename
        infile = open(cpu_filename).readlines()
        num_lines = len(infile)
        cpu_list = []
        time_list = []
        i = 0
        while i < num_lines:
            i += 1
            cpu_value = 0
            cpu_time = 0
            while i < num_lines and '---' not in infile[i]:
                if Config().package in infile[i]:
                    if float(infile[i].split()[2].strip('%')) <100:
                        cpu_value = float(infile[i].split()[2].strip('%'))
                    elif i==0:
                        cpu_value = 0
                    else:
                        cpu_value = cpu_list[len(cpu_list)-1]
                if 'Time pass:' in infile[i]:
                    cpu_time = int(infile[i].split()[-2])
                i += 1
            time_list.append(cpu_time)
            cpu_list.append(cpu_value)
        max_cpu = max(cpu_list)
        min_cpu = min(cpu_list)
        median_cpu = numpy.average(cpu_list)

        report = [cpu_list, time_list, max_cpu, min_cpu, median_cpu]
        return report

    def bty_usage_log_parser(self):
        bty_log_filename = self.log_directory + "/" + Config().btyFilename
        bty_level_list = []
        time_list = []
        infile = open(bty_log_filename).readlines()
        num_lines = len(infile)
        i = 0
        while i < num_lines:
            bty_level = -1
            i += 1
            btr_time = 0
            while i < num_lines and '---' not in infile[i]:
                if 'level:' in infile[i]:
                    bty_level = int(infile[i].strip().split()[-1])
                if 'Time pass:' in infile[i]:
                    btr_time = int(infile[i].split()[-2])
                i += 1
            bty_level_list.append(bty_level)
            time_list.append(btr_time)
        max_bat = max(bty_level_list)
        min_bat = min(bty_level_list)
        diff_bat = (max_bat - min_bat)
        report = [bty_level_list, time_list, max_bat, min_bat, diff_bat]
        return report

    def bty_temp_log_parser(self):
        bty_log_filename = self.log_directory + "/" + Config().btyFilename
        bty_tmpt_list = []
        time_list = []
        infile = open(bty_log_filename).readlines()
        num_lines = len(infile)
        i = 0
        while i < num_lines:
            bty_temp = -1
            i += 1
            btr_time = 0
            while i < num_lines and '---' not in infile[i]:
                if 'temperature:' in infile[i]:
                    bty_temp = int(infile[i].strip().split()[-1])
                if 'Time pass:' in infile[i]:
                    btr_time = int(infile[i].split()[-2])
                i += 1
            bty_tmpt_list.append(bty_temp)
            time_list.append(btr_time)
        max_temp = max(bty_tmpt_list)
        min_temp = min(bty_tmpt_list)
        diff_temp = (max_temp - min_temp)

        report = [bty_tmpt_list, time_list, max_temp, min_temp, diff_temp]
        return report

    def data_log_parser(self):
        data_log_filename = self.log_directory + "/" + Config().dtuFilename
        background_rx = []
        background_tx = []
        foreground_rx = []
        foreground_tx = []
        time_list = []
        infile = open(data_log_filename).readlines()
        num_lines = len(infile)
        i = 0
        while i < num_lines:
            while i < num_lines and '---' not in infile[i]:
                i += 1
            if i >= num_lines:
                break
            i += 1
            background_rx_mbbytes = - 0.1
            background_tx_mbbytes = - 0.1
            foreground_rx_mbbytes = - 1
            foreground_tx_mbbytes = - 1

            while i < num_lines and '---' not in infile[i]:
                if 'background_rx_bytes' in infile[i]:
                    background_rx_mbbytes = int(infile[i].split("=")[-1].strip())/1024/1024
                if 'background_tx_bytes' in infile[i]:
                    background_tx_mbbytes = int(infile[i].split("=")[-1].strip())/1024/1024
                if 'foreground_rx_bytes' in infile[i]:
                    foreground_rx_mbbytes = int(infile[i].split("=")[-1].strip())/1024/1024
                if 'foreground_tx_bytes' in infile[i]:
                    foreground_tx_mbbytes = int(infile[i].split("=")[-1].strip())/1024/1024
                if 'Time pass:' in infile[i]:
                    times = int(infile[i].split()[-2])
                i += 1

            background_rx.append(background_rx_mbbytes)
            background_tx.append(background_tx_mbbytes)
            foreground_rx.append(foreground_rx_mbbytes)
            foreground_tx.append(foreground_tx_mbbytes)
            time_list.append(times)
        data = [background_rx, background_tx, foreground_rx, foreground_tx]
        report = [data, time_list]

        return report

    def events_parser(self):
        events_dir_path = Folders().events_folders_creation(self.log_directory)

        for event_name in Config().events_list:

            log_captured = events_dir_path+"/log_captured.txt"
            os.system("grep -i \""+event_name+"\" "+self.log_directory+"/*"+"com.verizon"+"* > " + log_captured)

            results_file = events_dir_path+"/"+event_name+".txt"
            output = open(results_file, "w")
            n = 0
            for line in open(log_captured):
                if len(line) > 2:
                    n+=1
                    str1 = line[line.find(event_name):line.find(event_name)+len(event_name)]
                    line = line.split()
                    epoch = line[2]
                    local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(epoch)))
                    output.write(" epoch="+epoch+" ---> Local time = "+local_time+"   "+str1+"   "+str(n))
                    output.write("\n")
                    output.write("===========================================================================\n")
            output.close()
            os.system("rm "+log_captured)
            # print(event_name + " - " + str(n))

        event_report_name = []
        event_report_quant = []

        for event_name in Config().events_list:
            log_captured = events_dir_path+'/'+event_name+'.txt'
            n = 0
            for line in open(log_captured):
                if line>2 and line.find('epoch')!=-1:
                    n+=1
            event_report_name.append(str(event_name))
            event_report_quant.append(n)
        report = [event_report_name, event_report_quant]
        return report

