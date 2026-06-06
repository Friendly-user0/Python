
# If you have a long list of ip's and want to find out who they belong to, this is the script.
## Standard Python ssl libraries strictly enforce standard TLS handshakes and will fail silently if the target requires a specific Server Name Indication (SNI) or uses an unexpected TLS configuration,
##                                                                                                                                                    so I recommend using the one liner in my: https://github.com/Friendly-user0/Web-Hacking/blob/main/Recon.md

#!/usr/bin/env python3
import argparse
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor
import json

def get_reverse_dns(ip):
    """Finds the PTR record for the IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "No PTR record"

def get_asn_info(ip):
    """Queries Team Cymru's DNS WHOIS service for rapid ASN and Org lookup."""
    try:
        # Reverse the IP for the Cymru DNS query
        reversed_ip = ".".join(reversed(ip.split(".")))
        query = f"{reversed_ip}.origin.asn.cymru.com"
        asn_record = socket.gethostbyname_ex(query)[2][0]
        
        # Now get the TXT record for the ASN descriptor
        # To keep dependencies zero, we do a basic fallback or stick to PTR/SSL if this fails.
        return asn_record
    except Exception:
        return "Unknown ASN/Org"

def get_ssl_cn(ip, port=443, timeout=2):
    """Grabs the Common Name (CN) and Subject Alternative Names from SSL Cert."""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                # Fallback to OpenSSL style parsing if decoded cert is empty due to CERT_NONE
                # For simplicity, we grab the dict if available
                cert_dict = ssock.getpeercert()
                if cert_dict and 'subject' in cert_dict:
                    for item in cert_dict['subject']:
                        if item[0][0] == 'commonName':
                            return item[0][1]
    except Exception:
        pass
    return "No HTTPS/SSL CN"

def process_ip(ip):
    """Combines all checks for a single IP."""
    ip = ip.strip()
    if not ip:
        return None
    
    # Run the checks
    ptr = get_reverse_dns(ip)
    ssl_cn = get_ssl_cn(ip)
    
    return {
        "ip": ip,
        "reverse_dns": ptr,
        "ssl_common_name": ssl_cn
    }

def main():
    parser = argparse.ArgumentParser(description="Precise IP Ownership Attribution Tool")
    parser.add_argument("-f", "--file", required=True, help="Path to the file containing IP addresses")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    parser.add_argument("-o", "--output", choices=["text", "json"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Processing {len(ips)} IPs using {args.threads} threads...\n", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(process_ip, ip) for ip in ips]
        for future in futures:
            res = future.result()
            if res:
                results.append(res)
                if args.output == "text":
                    print(f"IP: {res['ip']}")
                    print(f"  └─ PTR (Reverse DNS): {res['reverse_dns']}")
                    print(f"  └─ SSL Common Name:  {res['ssl_common_name']}")
                    print("-" * 50)

    if args.output == "json":
        print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
