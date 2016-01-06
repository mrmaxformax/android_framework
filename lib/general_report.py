from test_framework.soak import *
def general():
    report_dir= '../Report/1'
    cmd = 'mkdir test %s' % report_dir
    os.system(cmd)
