
from lib.apk_process import *

def multi_soak():
    count = 0
    for ipp in (Connection().get_devices()):
        time.sleep(1)
        if '.' in ipp:
            ip = ipp[:-5]
            count += 1
            t = threading.Thread(target=soak, args=(ip, count))
            t.start()

def soak(ip, count):
    port = config['port']
    build = Connection().get_package_version(ip, port)
    device = get_device_name(ip)
    log_directory = Folders().folders_creation(build, device)
    get_device_logs(ip, port, log_directory,  device, count)
    time.sleep(60)
    Connection().pull_log(log_directory, ip, port, device)
    time.sleep(60)
    Parser(log_directory, device, build).collect_report()

def get_device_logs(ip, port, log_directory, device, count):
    duration = config['duration']
    start = time.time()
    endtime = time.time() + float(duration)*60
    regendtime = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S.%f')
    print(str(count)+' Soak is runing on %s %s and finish %s' % (ip, device, regendtime[10:-7]))
    memLoghandler = open(os.path.join(log_directory, Config().memFilename), 'w')
    cpuLoghandler = open(os.path.join(log_directory, Config().cpuFilename), 'w')
    batLoghandler = open(os.path.join(log_directory, Config().btyFilename), 'w')
    dtuLoghandler = open(os.path.join(log_directory, Config().dtuFilename), 'w')
    while time.time() < endtime:
        t1 = threading.Thread(target=usage(device, ip, port, cpuLoghandler, start, Config().cpuName, Config().cpuAdb),
                              args=(ip, cpuLoghandler))
        t1.start()

        t2 = threading.Thread(target=usage(device, ip, port, memLoghandler, start, Config().memName, Config().memAdb),
                              args=(ip, memLoghandler))
        t2.start()

        t3 = threading.Thread(target=usage(device, ip, port, batLoghandler, start, Config().batName, Config().batAdb),
                              args=(ip, batLoghandler))
        t3.start()

        t4 = threading.Thread(target=data_usage(device, ip, port, dtuLoghandler, start, Config().dataName,
                                                Config().dataAdb), args=(ip, dtuLoghandler))
        t4.start()

with open('devices.json') as config:
    config = json.load(config)

