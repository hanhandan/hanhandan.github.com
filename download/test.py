import  os
import  sys
import  tty, termios
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
ch='hello'

while True:
    ch = sys.stdin.readline()
    print ch
    if cmp(str(ch),"quit") == 0:
        break
