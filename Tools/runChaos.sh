#!/bin/bash

# Check if a file argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domains_file.txt>"
    exit 1
fi

INPUT_FILE="$1"

# Check if the file actually exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1

fi

# Read the file line by line
while IFS= read -r domain || [ -n "$domain" ]; do
    # Strip any hidden carriage returns (CRLF from Windows files) and whitespace
    domain=$(echo "$domain" | tr -d '\r' | xargs)

    # Skip empty lines
    if [ -z "$domain" ]; then
        continue
    fi

    echo "Scanning: $domain..."

    # Run chaos and save to {domain}.txt
    chaos -d "$domain" -o "${domain}.txt"

    echo "Finished $domain. Sleeping for 1 second..."
    sleep 1
    echo "----------------------------------------"

done < "$INPUT_FILE"

echo "All targets processed!"
