import sys,tty, os, time

while(True):
    time.sleep(0.010)
    
    tty.setcbreak(sys.stdin)
    key = ord(sys.stdin.read(1))

    if key==113:
        break
    else:
        key = ord(sys.stdin.read(1))  # key captures the key-code
        # based on the input we do something - in this case print something
        print(key)

os.system('stty sane')
sys.exit(0)
