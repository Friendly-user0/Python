### VIBE CODED SCRIPT ###

#!/usr/bin/env python3
import argparse
import requests
import time
import sys

def banner():
    print("""
    ======================================
            EnJOY THE NONSENSE
    ======================================
    """)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and filter URLs from AlienVault OTX for a specific subdomain.")
    
    # Required arguments
    parser.add_argument("-d", "--domain", required=True, help="The main domain to query (e.g., example.com)")
    parser.add_argument("-t", "--target", required=True, help="The specific subdomain to filter for (e.g., test.example.com)")
    
    # Optional arguments with nice defaults
    parser.add_argument("-p", "--pages", type=int, default=5, help="Number of pages to increment through (Default: 5)")
    parser.add_argument("-l", "--limit", type=int, default=2000, help="Results limit per API request (Default: 2000)")
    parser.add_argument("-o", "--output", help="Save unique results to a file")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay in seconds between requests to avoid rate limits (Default: 0.5)")
    
    return parser.parse_args()

def fetch_page(domain, page, limit):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list"
    params = {
        "limit": limit,
        "page": page
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print(f"[!] Blocked or rate limited on page {page}. Try increasing --delay.")
            return None
        else:
            print(f"[!] Error on page {page}: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[!] Request failed on page {page}: {e}")
        return None

def main():
    banner()
    args = parse_args()
    
    unique_urls = set()
    
    print(f"[*] Querying OTX for base domain: {args.domain}")
    print(f"[*] Filtering for target: {args.target}")
    print(f"[*] Scraping up to {args.pages} pages...\n")
    
    for page in range(1, args.pages + 1):
        print(f"[+] Fetching page {page}/{args.pages}...", end="\r")
        sys.stdout.flush()
        
        data = fetch_page(args.domain, page, args.limit)
        
        if not data or "url_list" not in data:
            print(f"\n[!] No data returned or end of results on page {page}.")
            break
            
        url_list = data["url_list"]
        if not url_list:
            print(f"\n[*] Reached the end of available data at page {page}.")
            break
            
        # Filter URLs on the fly
        for item in url_list:
            url = item.get("url", "")
            if args.target in url:
                unique_urls.add(url)
                
        # Politeness delay
        time.sleep(args.delay)
        
    print(f"\n\n[*] Completed! Found {len(unique_urls)} unique URLs matching '{args.target}'.")
    
    # Sort the results
    sorted_urls = sorted(list(unique_urls))
    
    # Output to stdout or file
    if args.output:
        with open(args.output, "w") as f:
            for url in sorted_urls:
                f.write(url + "\n")
        print(f"[+] Saved results to {args.output}")
    else:
        print("\n--- Discovered URLs ---")
        for url in sorted_urls:
            print(url)

if __name__ == "__main__":
    main()
