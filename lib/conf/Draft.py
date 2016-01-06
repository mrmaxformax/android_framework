'''



 # Connection().kill_server()
        # Connection().power_off(1)
        # time.sleep(5)
        # Connection().usb_off(1)
        # time.sleep(60)
        # Connection().usb_on(1)
        # time.sleep(55)
        # Connection().power_on(1)
        # time.sleep(60)
        # Connection().start_server()
        # time.sleep(10)
        # print len(Connection().get_devices())
        # devices_connected_names()
        # time.sleep(20)
        # connect_all_devices()
        # time.sleep(10)
        # connect_devices_wifi()
        # time.sleep(10)




http://clientbuilds.oncue.verizon.net/builds.php
https://github.oncue.verizon.net/rusual/samsung

def main_soak():
    threads = []
    count = 0
    for ipp in (Connection().get_devices()):
        time.sleep(1)
        if '.' in ipp:
            ip = ipp[:-5]
            count += 1
            t = threading.Thread(target=main, args=(ip, count))
            threads.append(t)
            t.start()


def get_num_dev_connected():
    return len(Connection().get_devices())


def check_devices():
    num_devices = get_num_dev_connected()
    if num_devices == config['totalDevices']:
        print 'All devices is Connected'
    else:
        print 'Not all devices connected'


def touch(ip, ca, prm, attempts):
    for i in range(attempts):
        if prm['id'] in json.loads(ca.run(cmd='CurrentPage.MobileGetIds'))['result']:
            ca.run(cmd='Command.Touch', prm=prm)
            return
        else:
            time.sleep(1)
    if prm['id'] == 'ModalCancelButton':
        return
    else:
        # Connection().get_screenshot(ip, '5555')
        exit('UI element not found %s on device %s' % (prm['id'], ip))



def run_websocket():
    threads = []
    count = 0
    for ipp in (Connection().get_devices()):
        time.sleep(1)
        if '.' in ipp:
            ip = ipp[:-5]
            count += 1
            t = threading.Thread(target=run_content_ts, args=(ip, count))
            threads.append(t)
            t.start()
            time.sleep(1)


def run_content(ip, count):
    Connection().shell_command('am force-stop com.verizonmedia.go90.enterprise', ip, '5555')
    time.sleep(2)
    print "%s Starting app on device: %s" % (count, ip)
    Connection().shell_command(Config().startapp, ip, '5555')
    time.sleep(15)
    ca = SQAHookConnection(ip)
    time.sleep(2)
    touch(ip, ca, {'id': 'LoginButton'}, 10)
    touch(ip, ca, {'id': 'EmailTextField'}, 10)
    ca.run(cmd='Command.Type', prm={'id': 'EmailTextField', 'text': 'katiarusu1710@gmail.com'})
    ca.run(cmd='Command.Type', prm={'id': 'PasswordTextField', 'text': 'Aa123456'})
    ca.run(cmd='Command.Touch', prm={'id': 'SignInButton'})
    touch(ip, ca, {'id': 'ModalCancelButton'}, 10)
    touch(ip, ca, {'id': 'Tab3Button'}, 10)
    touch(ip, ca, {'id': 'ProfileTabs', 'index': 1}, 10)
    time.sleep(2)
    touch(ip, ca, {'id': 'Grid', 'index': 0}, 10)
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    exit_go90(2, 30)
    time.sleep(2)
    Connection().shell_command(Config().startapp, ip, '5555')
    time.sleep(15)
    touch(ip, ca, {'id': 'Tab3Button'}, 10)
    touch(ip, ca, {'id': 'ProfileTabs', 'index': 0}, 10)
    touch(ip, ca, {'id': 'Grid', 'index': 0}, 10)
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    time.sleep(2)
    video_duration = json.loads(ca.run(cmd='System.GetTransportInfoFromPlayer'))['result']['endTime']
    if video_duration == 0:
        print('%s Video duration is 0 on device %s' % (count, ip))
        # Connection().get_screenshot(ip, '5555')
    else:
        if video_duration <= config['duration']*60-360:
            for i in range((config['duration']*60-360) / video_duration):
                time.sleep(video_duration)
                while 'MsgScreenReplay' not in json.loads(ca.run(cmd='CurrentPage.MobileGetIds'))['result']:
                    time.sleep(1)
                ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
        print '%s Video long enough on device %s' % (count, ip)


def run_content_old(ip, count):
    # Connection().shell_command('am force-stop com.verizonmedia.go90.enterprise', ip, '5555')
    # time.sleep(5)
    print "%s Starting app on device: %s" % (count, ip)
    Connection().shell_command(Config().startapp, ip, '5555')
    time.sleep(15)
    ca = SQAHookConnection(ip)
    # touch(ip, ca, {'id': 'LoginButton'}, 10)
    # touch(ip, ca, {'id': 'EmailTextField'}, 10)
    # ca.run(cmd='Command.Type', prm={'id': 'EmailTextField', 'text': 'katiarusu1710@gmail.com'})
    # ca.run(cmd='Command.Type', prm={'id': 'PasswordTextField', 'text': 'Aa123456'})
    # ca.run(cmd='Command.Touch', prm={'id': 'SignInButton'})
    touch(ip, ca, {'id': 'ProfileNavButton'}, 10)
    touch(ip, ca, {'id': 'ProfileTabs', 'index': 1}, 10)
    time.sleep(10)
    touch(ip, ca, {'id': 'Grid', 'index': 1}, 10)
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    exit_go90(2, 30)
    time.sleep(2)
    Connection().shell_command(Config().startapp, ip, '5555')
    time.sleep(15)
    touch(ip, ca, {'id': 'ProfileNavButton'}, 10)
    touch(ip, ca, {'id': 'ProfileTabs', 'index': 0}, 10)
    touch(ip, ca, {'id': 'Grid', 'index': 0}, 10)
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'PlayButton'})
    time.sleep(2)
    ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
    time.sleep(2)
    video_duration = json.loads(ca.run(cmd='System.GetTransportInfoFromPlayer'))['result']['endTime']
    if video_duration == 0:
        print('%s Video duration is 0 on device %s' % (count, ip))
        # Connection().get_screenshot(ip, '5555')
    else:
        if video_duration <= config['duration']*60-360:
            for i in range((config['duration']*60-360) / video_duration):
                time.sleep(video_duration)
                while 'MsgScreenReplay' not in json.loads(ca.run(cmd='CurrentPage.MobileGetIds'))['result']:
                    time.sleep(1)
                ca.run(cmd='Command.Touch', prm={'id': 'MsgScreenReplay'})
        print '%s Video long enough on device %s' % (count, ip)
'''
