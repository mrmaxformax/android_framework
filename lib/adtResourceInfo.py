
from connection import *
import sys, time
from utils import *

strftime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def usage(device, ip, port, log_handler, start, procName, adbCommand):
    out, ret, err = Connection().shell_command(adbCommand, ip, port)
    #print('\n===' + procName + '===')
    if ret != 0:
        print('%s. Can not get %s in %s.' % (err.rstrip('\r\n'), procName, device))
        sys.exit(0)
    #print("OK! - %s %s" % (device, strftime))
    log_handler.write('---' + strftime + '\n')
    log_handler.write(out)
    log_handler.write('Time pass: %s sec\n\n' % int(time.time() - start))


def data_usage(device, ip, port, log_handler, start, procName, adbCommand):
    out, ret, err = Connection().shell_command(adbCommand, ip, port)
    #print('\n===' + procName + '===')
    if ret != 0:
        print('%s. Can not get %s in %s.' % (err.rstrip('\r\n'), procName, device))
        sys.exit(0)
    #print("OK! - %s %s" % (device, strftime))
    tmpName = 'log_' + ip + '.txt'
    UID = Connection().uid(ip, port)
    log = open(tmpName, 'w')
    log.write(out)
    log.flush()
    log.close()

    if os.path.isfile(tmpName):
        infile = open(tmpName).readlines()
        log_handler.write("---" + strftime + "\n")

        for i in range(len(infile)):

            if infile[i].split()[3] == UID:

                if infile[i].split()[4] == str(0):  # cnt_set = 0 for background
                    background_rx_bytes = infile[i].split()[5]
                    background_tx_bytes = infile[i].split()[7]
                    log_handler.write('background_rx_bytes = ' + background_rx_bytes + '\n')
                    log_handler.write('background_tx_bytes = ' + background_tx_bytes + '\n')
                    #print('background_rx_bytes = ', background_rx_bytes)
                    #print('background_tx_bytes = ', background_tx_bytes)

                if infile[i].split()[4] == str(1):  # cnt_set = 1 for foreground
                    foreground_rx_bytes = infile[i].split()[5]
                    foreground_tx_bytes = infile[i].split()[7]
                    log_handler.write('foreground_rx_bytes = ' + foreground_rx_bytes + '\n')
                    log_handler.write('foreground_tx_bytes = ' + foreground_tx_bytes + '\n')
                    #print('foreground_rx_bytes = ', foreground_rx_bytes)
                    #print('foreground_tx_bytes = ', foreground_tx_bytes)
            log_handler.write('Time pass: %s sec\n\n' % int(time.time() - start))
    os.remove(tmpName)
