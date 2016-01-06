from soak import *
from lib.apk_process import *

def non_stop():
    while True:
        real_time("Start Soak Test on Hub 1 at ")
        test_case_hub1()
        time.sleep(10800)

def test_case_hub1():
    user_name = config['hub1_username']
    password = config['hub1_password']
    hub = 'hub1'

    download_apk()
    Connection().kill_server()
    Connection().power_off(sensor=1)
    Connection().usb_off(sensor=1)
    time.sleep(10)

    Connection().usb_on(sensor=1)
    Connection().power_on(sensor=1)
    time.sleep(10)

    Connection().start_server()
    connect_all_devices(hub=hub)
    print('All devices Uninstall app')
    all_devices_id(target=Connection().uninstall)
    print('All devices Install app')
    all_devices_id(target=Connection().install)
    time.sleep(5)

    print('All devices Start Reboot')
    all_devices_id(target=reboot_device)
    print('All devices Rebooted')
    time.sleep(30)

    all_devices_id(target=open_port_5555)
    print('All devices tcpip 5555')
    time.sleep(5)

    connect_devices_wifi(hub=hub, usb=1)
    time.sleep(5)
    Connection().shell_command('input tap 1095 1485', '192.168.75.127:5555')
    connect_devices_wifi(hub=hub, usb=1)

    multi_soak()

    Process(target=finish, args=(config['duration']*60+150, )).start()
    Process(target=create_report, args=((config['duration']*60+200), hub)).start()
    time.sleep(20)

    Connection().shell_command('input tap 1100 1400', '192.168.75.127:5555')
    time.sleep(1)

    all_devices_login(target=run_cut, user_name=user_name, password=password)

    exit_app_all_devices(times=2, delay=20)
    Process(target=exit_app_all_devices, args=(3, (config['duration']*56))).start()
    all_devices_ip(target=start_app)
    all_devices_ip(target=run_1hour_video)

if __name__ == "__main__":
    test_case_hub1()
    # non_stop()