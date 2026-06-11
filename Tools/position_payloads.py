import os
import itertools

def generate_scenarios(dimensions, num_accounts=2):
    """
    Generates a systematic matrix where we vary elements across accounts.
    Starts at baseline (all Account 1), then systematically changes 1 field,
    then 2 fields, up to changing all fields to other accounts.
    """
    # Create lists of account indices, e.g., [0, 1] for 2 accounts
    account_indices = list(range(num_accounts))
    
    # Generate every single mathematical combination across the dimensions
    # For 4 dimensions and 2 accounts, this is 2^4 = 16 combinations
    raw_combos = list(itertools.product(account_indices, repeat=dimensions))
    
    # Sort the combinations by the number of modifications away from Account 1 (index 0)
    # This guarantees the "Layer" order: Baseline -> 1 change -> 2 changes -> etc.
    sorted_combos = sorted(raw_combos, key=lambda x: sum(1 for idx in x if idx != 0))
    return sorted_combos

def main():
    print("====================================================")
    print("   Universal Multi-Account Matrix Generator         ")
    print("====================================================")
    
    # 1. Ask for the number of accounts
    try:
        num_accounts = int(input("[+] How many testing accounts do you have? (e.g., 2, 3, 4): "))
        if num_accounts < 2:
            print("[-] You need at least 2 accounts to perform cross-isolation testing.")
            return
    except ValueError:
        print("[-] Invalid number entry.")
        return

    # 2. Ask for the number of placeholders
    try:
        dimensions = int(input("[+] How many Identification placeholders/positions? (Max 5): "))
        if dimensions < 1 or dimensions > 5:
            print("[-] Please choose a placeholder count between 1 and 5.")
            return
    except ValueError:
        print("[-] Invalid number entry.")
        return

    # 3. Collect data dynamically based on user input
    # Structure: pool[placeholder_index][account_index]
    pool = [[] for _ in range(dimensions)]
    
    for acc in range(1, num_accounts + 1):
        print(f"\n--- DATA FOR ACCOUNT #{acc} ---")
        for dim in range(1, dimensions + 1):
            val = input(f"    Enter value for Identification {dim}: ").strip()
            while not val:
                print(f"    [!] Value cannot be empty.")
                val = input(f"    Enter value for Identification {dim}: ").strip()
            pool[dim - 1].append(val)

    # 4. Generate the structured alignment matrix
    scenario_indices = generate_scenarios(dimensions, num_accounts)
    
    # Initialize empty tracking buckets for each output file
    file_buckets = [[] for _ in range(dimensions)]
    
    for combo in scenario_indices:
        # combo is something like (0, 0, 1, 0) meaning Acc1, Acc1, Acc2, Acc1
        for dim_idx, acc_idx in enumerate(combo):
            actual_value = pool[dim_idx][acc_idx]
            file_buckets[dim_idx].append(actual_value)

    # 5. Write the distinct files
    print("\n[+] Exporting separate positioning files...")
    for dim_idx in range(dimensions):
        filename = f"position{dim_idx + 1}_Identification.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for item in file_buckets[dim_idx]:
                f.write(item + "\n")
        print(f"    -> Saved {len(file_buckets[dim_idx])} lines to {filename}")

    print("\n====================================================")
    print(f"[++] Complete! Total generated test iterations per file: {len(scenario_indices)}")
    print("[++] Load these files sequentially into your Pitchfork sets.")
    print("====================================================")

if __name__ == "__main__":
    main()
