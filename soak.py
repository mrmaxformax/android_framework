import string
from lib.sqahook_communicate import *
from lib.createReport import Graphs
from multiprocessing import Process
import threading
from lib.adtResourceInfo import *
from lib.adtLogParser import *
from lib.connection import *
from lib.utils import *

def usb_and_power_on(delay, sensor):
    time.sleep(delay)
    real_time("USB and Power ON ")
    Connection().usb_on(sensor)
    time.sleep(5)
    Connection().power_on(sensor)
    time.sleep(5)
def finish(delay):
    time.sleep(delay)
    all_devices_ip(start_app)
    time.sleep(10)
    all_devices_ip(play)
def devices_connected_names():
    for i in Connection().get_devices():
        try:
            print get_device_name(i)
        except KeyError:
            print "  Devices not in config"
def all_devices_login(target, user_name, password):
    threads = []
    count = 0
    for ipp in (Connection().get_devices()):
        if '.' in ipp:
            ip = ipp[:-5]
            count += 1
            t = Thread(target=target, args=(ip, user_name, password))
            threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
def run_cut(ip, user_name, password):
    # print('%s start run cut on %s' % (count, get_device_name(ip)))
    ca = SQAHookConnection(ip)
    ca.run(cmd="System.SetStorageValue", prm={"key":"file/GovernorEnvironment","value":config['env']+".governor.oncue.com"})
    ca.run(cmd="System.SetStorageValue", prm={"key":"file/isTestUser","value":True})
    ca.run(cmd="System.GetStorageValue", prm={"key":"file/GovernorEnvironment"})
    ca.run(cmd="System.GetStorageValue", prm={"key":"file/isTestUser"})
    ca.run(cmd="System.Restart")
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'LoginButton'})
    time.sleep(2)
    ca.run(cmd='Command.Type', prm={'id': 'EmailTextField', 'text': user_name})
    time.sleep(1)
    ca.run(cmd='Command.Type', prm={'id': 'PasswordTextField', 'text': password})
    time.sleep(1)
    ca.run(cmd='Command.Touch', prm={'id': 'SignInButton'})
    time.sleep(5)
    Connection().shell_command('input tap 1100 1400', '192.168.75.127:5555')
    ca.run(cmd='Command.Touch', prm={'id': 'ModalCancelButton'})  # Skip Pop-up
    time.sleep(5)
    # raw_input('Tab profile button')
    # ca.run(cmd='Command.Touch', prm={'id': 'Tab3Button'})# old UI
    # time.sleep(1)
    ca.run(cmd="CurrentPage.SwitchMainTabs", prm={"index": 2})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'ProfileNavButton'}) # old UI
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'ProfileTabs', 'index': 1})
    time.sleep(1)
    ca.run(cmd='Command.Touch', prm={'id': 'ProfileMomentsGrid', 'index': 0})
    time.sleep(3)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})  #Replay

def run_1hour_video(ip, count):
    # print "%s Starting 1 hour video on device %s" % (count, get_device_name(ip))
    ca = SQAHookConnection(ip)
    time.sleep(2)
    # ca.run(cmd='Command.Touch', prm={'id': 'Tab3Button'}) #old UI
    time.sleep(1)
    ca.run(cmd="CurrentPage.SwitchMainTabs", prm={"index": 2})
    time.sleep(5)
    ca.run(cmd='Command.Touch', prm={'id': 'Grid', 'index': 0})
    time.sleep(10)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})  # Play
    time.sleep(1)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})  # Replay
    time.sleep(50)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    # time.sleep(6)
    # video_duration = json.loads(ca.run(cmd='System.GetTransportInfoFromPlayer'))['result']['endTime']
    # time.sleep(1)
    # if video_duration == 0:
    #     print('%s Video duration is 0 on device %s' % (count, get_device_name(ip)))
    #     get_screenshot(ip)
    # else:
    #     if video_duration <= config['duration']*60-360:
    #         for i in range((config['duration']*60-360) / video_duration):
    #             # print ('wait %s for end video on %s' % (video_duration, get_device_name(ip)))
    #             time.sleep(video_duration-100)
    #             # while 'MsgScreenReplay' not in json.loads(ca.run(cmd='CurrentPage.MobileGetIds'))['result']:
    #             for i in range(20):
    #                 time.sleep(2)
    #                 # print ('while  %s' % get_device_name(ip))
    #             # print ('Click on rewach %s' % get_device_name(ip))
    #                 ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    #     # print('%s Video long enough on device %s' % (count, get_device_name(ip)))
def get_device_name(id_or_ip):
    devices = {key: value for key, value in config.items() if key == 'devices'}
    if id_or_ip.find('.') != -1:
        ret = {dev['ip']: dev['device'] for dev in devices['devices']}
    else:
        ret = {dev['id']: dev['device'] for dev in devices['devices']}
    return ret[id_or_ip]
def total_devices_config(hub):
    devices = {key: value for key, value in config.items() if key == hub}
    n = 0
    for dev in devices[hub]:
        n += 1
    return n
def kill_app(ip, count):
    print '%s kill app on %s' % (count, get_device_name(ip))
    Connection().shell_command('am force-stop com.verizonmedia.go90.enterprise', ip, config['port'])
    time.sleep(2)
def start_app(ip, count):
    # print '%s start app on %s' % (count, get_device_name(ip))
    Connection().shell_command(Config().startapp, ip, config['port'])
    time.sleep(10)
def real_time(note):
    start = time.time()
    reg = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    print(note + reg)
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
    # real_time("Start parser ")
    Parser(log_directory, device, build).collect_report()
    # real_time('Finishi parsing ')
def get_device_logs(ip, port, log_directory, device, count):
    duration = config['duration']
    start = time.time()
    endtime = time.time() + float(duration)*60
    regendtime = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S.%f')
    print str(count)+' Soak is runing on %s %s and finish %s' % (ip, device, regendtime[10:-7])
    memLoghandler = open(os.path.join(log_directory, Config().memFilename), 'w')
    cpuLoghandler = open(os.path.join(log_directory, Config().cpuFilename), 'w')
    batLoghandler = open(os.path.join(log_directory, Config().btyFilename), 'w')
    dtuLoghandler = open(os.path.join(log_directory, Config().dtuFilename), 'w')
    while time.time() < endtime:
        t1 = threading.Thread(target=usage(device, ip, port, cpuLoghandler, start, Config().cpuName, Config().cpuAdb), args=(ip, cpuLoghandler))
        t1.start()

        t2 = threading.Thread(target=usage(device, ip, port, memLoghandler, start, Config().memName, Config().memAdb), args=(ip, memLoghandler))
        t2.start()

        t3 = threading.Thread(target=usage(device, ip, port, batLoghandler, start, Config().batName, Config().batAdb), args=(ip, batLoghandler))
        t3.start()

        t4 = threading.Thread(target=data_usage(device, ip, port, dtuLoghandler, start, Config().dataName, Config().dataAdb), args=(ip, dtuLoghandler))
        t4.start()
def connect_devices_wifi(hub, usb=None):
    if usb is not None:
        devices = total_devices_config(hub) * 2
    else:
        devices = total_devices_config(hub)
    while len(Connection().get_devices()) != devices:
        for x in range(0, total_devices_config(hub)):
            ip = config[hub][x]['ip']
            if ip + ":" + config['port'] not in Connection().get_devices():
                Connection().connect_via_ip(ip)
                # print 'Try to connect over WiFi device %s' % get_device_name(ip)
                time.sleep(5)
    print 'Connected all %s devices over wifi' % len(Connection().get_devices())
def all_devices_ip(target):
    threads = []
    count = 0
    for ipp in (Connection().get_devices()):
        if '.' in ipp:
            ip = ipp[:-5]
            count += 1
            t = Thread(target=target, args=(ip, count))
            threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
def all_devices_id(target):
    threads = []
    for id in (Connection().get_devices()):
        if "." not in id:
            t = Thread(target=target, args=(id,))
            threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
def connect_all_devices(hub):
    Connection().kill_server()
    time.sleep(2)
    Connection().start_server()
    time.sleep(4)
    while len(Connection().get_devices()) != total_devices_config(hub):
        print('Waiting for all devices')
        time.sleep(2)
    print('Connected all %s devices' % len(Connection().get_devices()))
def reboot_device(id):
    Connection().adb_command('reboot', id)
    while id not in Connection().get_devices():
        time.sleep(1)
def open_port_5555(id):
    Connection().adb_command_tcp('tcpip', id, '5555')
    for i in range(10):
        if 'LISTEN' not in str(Connection().shell_command('netstat -an | grep " tcp"', id)):
            time.sleep(1)
def unlock_device(id):
    Connection().shell_command('input swipe 550 1170 550 800', id)
    time.sleep(3)
    Connection().shell_command('input swipe 1000 1100 200 100', id)
    time.sleep(3)
    Connection().shell_command('input swipe 300 300 500 100', id)
    time.sleep(3)
    Connection().shell_command('input swipe 500 700 800 750', id)
    time.sleep(3)
    Connection().shell_command('input swipe 500 700 800 750', id)
    time.sleep(2)
    Connection().shell_command('input swipe 550 1170 550 800', id)
    time.sleep(2)
    Connection().shell_command('input swipe 300 300 500 100', id)
    time.sleep(2)
    Connection().shell_command('input swipe 1000 1100 200 100', id)
def exit_app_all_devices(times, delay):
    time.sleep(delay)
    for ip in (Connection().get_devices()):
        if '.' in ip:
            for i in range(times):
                Connection().shell_command('input keyevent 4', ip)
                time.sleep(1)
def create_report(delay,hub):
    time.sleep(delay)
    total_devices = total_devices_config(hub)
    count = 0
    for x in range(0, total_devices):
        device = config[hub][x]['device']
        log_directory = '../Report/%s' % device
        count += 1
        print str(count) + ' Start create report device ' + device
        Graphs(log_directory).start()
def play(ip, count):
    print('%s start cleanup on %s' % (count, get_device_name(ip)))
    ca = SQAHookConnection(ip)
    ca.run(cmd='Command.Touch', prm={'id': 'ModalCancelButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'Tab3Button'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'ProfileNavButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'Grid', 'index': 0})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
def power_login():
    asid = ''.join([random.choice(string.digits) for n in xrange(32)])
    ip = '" 192.168.24.109/login.cgi'
    curl1 = 'curl -X POST -d "username=ubnt&password=ubnt" -b "AIROS_SESSIONID='
    curl = curl1 + asid + ip
    os.system(curl)
    time.sleep(1)
    return asid
def power_on():
    curl1 = 'curl -X PUT -d output=1 -b "AIROS_SESSIONID='
    ip1 = '" 192.168.24.109/sensors/1'
    ip2 = '" 192.168.24.109/sensors/2'
    asid = power_login()
    curls1 = curl1 + asid + ip1
    os.system(curls1)
    time.sleep(1)
    curls2 = curl1 + asid + ip2
    os.system(curls2)
    time.sleep(1)
    print "Power ON"
def power_off():
    curl1 = 'curl -X PUT -d output=0 -b "AIROS_SESSIONID='
    ip1 = '" 192.168.24.109/sensors/1'
    ip2 = '" 192.168.24.109/sensors/2'
    asid = power_login()
    curls1 = curl1 + asid + ip1
    os.system(curls1)
    time.sleep(1)
    curls2 = curl1 + asid + ip2
    os.system(curls2)
    time.sleep(1)
    print "Power OFF"
def download_apk():
    os.system('rm -rf Go90-debug.apk')
    time.sleep(1)
    curl = 'curl -s -O ' + config['build_link'] + config['apk']
    os.system(curl)
    print 'APK V.%s DOWNLOADED' % curl[87:113]
def get_screenshot(ip):
    namescreen = '/sdcard/%s_%s.png' % (get_device_name(ip), time.strftime("%H:%M:%S"))
    screendir= 'screencap -p %s' % namescreen
    Connection().shell_command(screendir, ip, config['port'])
    ipp = ip + ':' + config['port']
    logdir = '../Report/%s' % get_device_name(ip)
    fullpath=Folders().all_subdirs_of(logdir)[0][0]
    cmd=['adb', '-s', ipp, 'pull', namescreen, fullpath]
    subprocess.call(cmd)
    rmscreen = 'rm %s' % namescreen
    Connection().shell_command(rmscreen, ip, config['port'])
def delit_last_report(ip, count):
    devicename = get_device_name(ip)
    logdir = '../Report/%s' % devicename
    fullpath=Folders().all_subdirs_of(logdir)[0][0]
    cmd = 'rm -rf %s' % fullpath
    os.system(cmd)
    print '%s Report was removed from %s' % (count, fullpath[10:])


with open('devices.json') as config:
    config = json.load(config)

