//free code camp

import sys #for command line arguments but performs a lot of things
import socket
from datetime import datetime

#defining target

if len(sys.argv) == 2:
        target = socket.gethostbyname(sys.argv[1]) #Translate a hostname to IPv4
else:
        print("Invalid amount of argument.")
        print("Syntax: python3 scanner.py <ip>")
        sys.exit()

# Adding  a pretty banner
print("-" * 50)
print("Scanning target "+target)
print("Time started: "+str(datetime.now()))
print("-" * 50)

try:
        for port in range(50,100):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1) # is float
                result = s.connect_ex((target.port)) #returns error indicator
                print("Checking port {}".format(port))
                if results == 0:
                                printf("Port {} is open".format(port))
                s.close()
except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()

except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()

except socket.error:
        print("Couldn't connect to server")
        sys.exit()

