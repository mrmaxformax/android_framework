from utils import *
import subprocess, sys, time, re, string, random
from threading import Thread, Event


class Connection:
    output = None
    error = None
    ret_code = 0
    devices = None

    def __init__(self):
        pass

    def kill_on_timeout(self, done, timeout, proc):
        if not done.wait(timeout):
            try:
                proc.kill()
            except OSError:
                pass

    def adb_command_tcp(self, cmd, ip=None, cmd1=None):
        done = Event()
        adb = Config().adb
        timeout = 5
        if ip is None:
            ret = [adb]
        else:
            ret = [adb, '-s', str(ip)]
        if isinstance(cmd, list):
            for i in cmd:
                ret.append(i)
        else:
            ret += [cmd]
        if cmd1 is not None:
            ret += [cmd1]
        adb_process = subprocess.Popen(ret, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        watcher = Thread(target=self.kill_on_timeout, args=(done, timeout, adb_process))
        watcher.daemon = True
        watcher.start()
        self.output, self.error = adb_process.communicate()
        self.ret_code = adb_process.returncode
        if len(self.output) == 0:
            self.output = None
        if len(self.error) == 0:
            self.error = None

        return self.output, self.ret_code, self.error

    def adb_command(self, cmd, ip=None, cmd1=None):
        adb = Config().adb

        if ip is None:
            ret = [adb]
        else:
            ret = [adb, '-s', str(ip)]
        if isinstance(cmd, list):
            for i in cmd:
                ret.append(i)
        else:
            ret += [cmd]

        if cmd1 is not None:
            ret += [cmd1]
        adb_process = subprocess.Popen(ret, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        self.output, self.error = adb_process.communicate()
        self.ret_code = adb_process.returncode

        if len(self.output) == 0:
            self.output = None

        if len(self.error) == 0:
            self.error = None
        return self.output, self.ret_code, self.error

    # BASE ADB SHELL COMMAND
    def shell_command(self, cmd, ip, port=None):
        if port is None:
            self.adb_command(['-s', str(ip), 'shell', str(cmd)])
        else:
            if len(ip.split('.')) == 4:
                self.adb_command(['-s', str(ip) + ':' + str(port), 'shell', str(cmd)])
            else:
                self.adb_command(['-s', str(ip), 'shell', str(cmd)])
        return self.output, self.ret_code, self.error

    # CONNECTION via WiFi
    def listen_tcp(self, port):
        self.adb_command(['tcpip', port])
        print(self.output)

    def connect_via_ip(self, ip, port=None):
        x = 0
        while x <= 5:
            if 'connected' in str(self.output):
                # print("  Device %s connected" % ip)
                break
            else:
                # print(' waiting feedback #' + str(x+1) + ' from phone')
                if port is None:
                    self.adb_command(['connect', "%s" % str(ip)])
                    time.sleep(2)
                else:
                    self.adb_command(['connect', "%s:%s" % (str(ip), str(port))])
                x +=1
        else:
            print("Not able to connect device %s" % ip)

    # ADB Start/Stop
    def start_server(self):
        self.adb_command('start-server')

    def kill_server(self):
        self.adb_command('kill-server')

    def get_devices(self):
        self.adb_command('devices')
        self.devices = self.output.partition('\n')[2].replace('device', '').split()
        if self.devices[1:] == ['no', 'permissions']:
            self.devices = None
        return self.devices

    # --
    def install_l(self, app=None):
        if app is None:
            return self.output
        cmd = 'install -l '
        cmd += app
        self.adb_command(cmd)

    # we check package version
    def get_package_version(self, ip, port):
        l = []
        cmd = 'dumpsys package' +' ' + Config().package +' ' + '| grep versionCode='
        time.sleep(1)
        self.shell_command(cmd, ip, port)
        time.sleep(2)
        if self.output is None:
            print(self.output)
            print("Oops! Have you installed our App on %s device?" % ip)
            Connection().get_package_version(ip, port)
            #sys.exit(0)
        else:
            for i in range(len(self.output.split())):
                if 'versionCode' in self.output.split()[i]:
                    uid = self.output.split()[i].split("=")[1]
                    l.append(uid)
        return l[0]

    # PACKAGE
    def uid(self, ip, port):
        l = []
        cmd = 'dumpsys package' +' ' + Config().package +' ' + '| grep userId='
        self.shell_command(cmd, ip, port)
        for i in range(len(self.output.split())):
            if 'userId' in self.output.split()[i]:
                uid = self.output.split()[i].split("=")[1]
                l.append(uid)
        return l[0]

    def uninstall(self, ip):
        self.adb_command(['uninstall', Config().package.encode("utf-8")], ip)

    def install(self, ip):
        self.adb_command(['install', Config().apk.encode("utf-8")], ip)


    # we get device manufacturer and model
    def manufacture(self, ip=None, port=None):
        time.sleep(1)
        cmd = Config().device_manufacture
        l1 = self.shell_command(cmd, ip, port)[0]
        cmd2 = Config().device_model
        l2 = self.shell_command(cmd2, ip, port)[0]
        n=3
        dev = ''
        while n>=0:
            if n==0:
                print('Sorry I can\'t get Manufacture name. Please check your phone %s' % l1)
                sys.exit(0)
            elif l2 is not None:
                dev = l1.capitalize().replace("\r\n","") +'_' + re.sub(r'\s|\n|\r', '', l2)
                break
            else:
                print('Try to get Manufacture name %s\'st time' %n)
                n -= 1
        return dev

    def pull_log(self, log_directory, ip, port, device):
        cmd = " -s " + ip + ":" + port + Config().logAdb + Config().package + ".log " + log_directory
        out, ret, err = self.adb_command(cmd.split())
        time.sleep(2)
        if 'KB/s' in err:
            print("OK! - Log file is downloaded from %s" % device)
        else:
            print('Can not get log file from %s.' % device)
        return self.output, self.ret_code, self.error

    @staticmethod
    def usb_on(sensor):
        curl = "curl -s 'http://192.168.24.116/cgi-bin/runcommand.sh?100:cmd=254,%s,1' &> /dev/null" % (107 + sensor)
        os.system(curl)
        time.sleep(1)
        print "USB HUB %s CONNECTED" % sensor

    @staticmethod
    def usb_off(sensor):
        curl = "curl -s 'http://192.168.24.116/cgi-bin/runcommand.sh?731:cmd=254,%s,1' &> /dev/null" % (99 + sensor)
        os.system(curl)
        time.sleep(1)
        print "USB HUB %s DISCONNECTED" % sensor

    @staticmethod
    def power_login():
        asid = ''.join([random.choice(string.digits) for n in xrange(32)])
        ip = '" 192.168.24.109/login.cgi'
        curl1 = 'curl -s -X POST -d "username=ubnt&password=ubnt" -b "AIROS_SESSIONID='
        curl = curl1 + asid + ip + ' &> /dev/null'
        os.system(curl)
        time.sleep(1)
        return asid

    @staticmethod
    def power_on(sensor):
        curl1 = 'curl -s -X PUT -d output=1 -b "AIROS_SESSIONID='
        ip = '" 192.168.24.109/sensors/%s' % sensor
        asid = Connection().power_login()
        curls = curl1 + asid + ip + ' &> /dev/null'
        os.system(curls)
        time.sleep(1)
        print "POWER CABLE CONNECTED TO HUB %s" % sensor

    @staticmethod
    def power_off(sensor):
        curl = 'curl -s -X PUT -d output=0 -b "AIROS_SESSIONID='
        ip = '" 192.168.24.109/sensors/%s' % sensor
        asid = Connection().power_login()
        curls = curl + asid + ip + ' &> /dev/null'
        os.system(curls)
        time.sleep(1)
        print "POWER CABLE DISCONNECTED FROM HUB %s" % sensor
