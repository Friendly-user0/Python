
# handy tool for wordlist haha...

import argparse

def generate_wordlists():
    parser = argparse.ArgumentParser(description="Generate synchronized wordlists for login counter resets.")
    
    # User Inputs
    parser.add_argument("-tu", "--target-user", required=True, help="Username to brute force (e.g., carlos)")
    parser.add_argument("-vu", "--valid-user", required=True, help="Your valid username (e.g., wiener)")
    parser.add_argument("-vp", "--valid-pass", required=True, help="Your valid password (e.g., peter)")
    parser.add_argument("-w", "--wordlist", required=True, help="File containing candidate passwords for the target")
    parser.add_argument("-i", "--interval", type=int, default=2, 
                        help="Number of target attempts before inserting valid credentials (default: 2)")

    args = parser.parse_args()

    try:
        with open(args.wordlist, 'r') as f:
            target_passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"[-] Error: {args.wordlist} not found.")
        return

    user_out = []
    pass_out = []
    
    current_batch = 0

    for p in target_passwords:
        # Every 'interval' attempts, insert the valid credentials first
        if current_batch == 0:
            user_out.append(args.valid_user)
            pass_out.append(args.valid_pass)
        
        # Add the target attempt
        user_out.append(args.target_user)
        pass_out.append(p)
        
        current_batch += 1
        
        # Reset batch counter once we reach the interval
        if current_batch >= args.interval:
            current_batch = 0

    # Write the files
    with open("users_payload.txt", "w") as f:
        f.write("\n".join(user_out))
    
    with open("passwords_payload.txt", "w") as f:
        f.write("\n".join(pass_out))

    print(f"[+] Done! Generated {len(user_out)} lines.")
    print("[+] Files created: users_payload.txt, passwords_payload.txt")

if __name__ == "__main__":
    generate_wordlists()
