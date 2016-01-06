import os
import string
from lib.sqahook_communicate import *
from lib.createReport import Graphs
from multiprocessing import Process
import threading
from lib.adtResourceInfo import *
from lib.adtLogParser import *
from lib.connection import *
from lib.utils import *


def download_apk():
    os.system('rm -rf XXX.apk') #remove in all catalogs without confirmation
    time.sleep(1)
    curl = 'curl -s -O ' + config['build_link'] + config['apk'] #connect to prod for downloading
    os.system(curl)
    print('APK V.%s DOWNLOADED' % curl[87:113])

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

def create_report(delay,hub):
    time.sleep(delay)
    total_devices = total_devices_config(hub)
    count = 0
    for x in range(0, total_devices):
        device = config[hub][x]['device']
        log_directory = '../Report/%s' % device
        count += 1
        print(str(count) + ' Start create report device ' + device)
        Graphs(log_directory).start()

def exit_app_all_devices(times, delay):
    time.sleep(delay)
    for ip in (Connection().get_devices()):
        if '.' in ip:
            for i in range(times):
                Connection().shell_command('input keyevent 4', ip)
                time.sleep(1)

def open_port_5555(id):
    Connection().adb_command_tcp('tcpip', id, '5555')
    for i in range(10):
        if 'LISTEN' not in str(Connection().shell_command('netstat -an | grep " tcp"', id)):
            time.sleep(1)

def reboot_device(id):
    Connection().adb_command('reboot', id)
    while id not in Connection().get_devices():
        time.sleep(1)

def connect_all_devices(hub):
    Connection().kill_server()
    time.sleep(2)
    Connection().start_server()
    time.sleep(4)
    while len(Connection().get_devices()) != total_devices_config(hub):
        print('Waiting for all devices')
        time.sleep(2)
    print('Connected all %s devices' % len(Connection().get_devices()))


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

def real_time(note):
    start = time.time()
    reg = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    print(note + reg)

def start_app(ip, count):
    # print '%s start app on %s' % (count, get_device_name(ip))
    Connection().shell_command(Config().startapp, ip, config['port'])
    time.sleep(10)



def finish(delay):
    time.sleep(delay)
    all_devices_ip(start_app)
    time.sleep(10)
    all_devices_ip(play)


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
    ca.run(cmd="System.SetStorageValue", prm={"key":"file/GovernorEnvironment","value":config['env']+".governor.XXXX.com"})
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


def get_device_name(id_or_ip):
    devices = {key: value for key, value in config.items() if key == 'devices'}
    if id_or_ip.find('.') != -1:
        ret = {dev['ip']: dev['device'] for dev in devices['devices']}
    else:
        ret = {dev['id']: dev['device'] for dev in devices['devices']}
    return ret[id_or_ip]

with open('devices.json') as config:
    config = json.load(config)