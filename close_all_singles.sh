#!/bin/bash

numbers_file="root_port_temp.txt"

if [ ! -f "$numbers_file" ]; then
    echo "Error: File '$numbers_file' not found."
    exit 1
fi

while IFS= read -r line; do
    echo "Shutting down on port number: $line"

    # Attempt to execute commands with different variations based on availability
    if command -v nc &>/dev/null; then
        echo "!EXIT" | nc 127.0.0.1 "$line"
    elif command -v ncat &>/dev/null; then
        echo "!EXIT" | ncat 127.0.0.1 "$line"
    elif [ -x ./netcat ]; then
        echo "!EXIT" | ./netcat 127.0.0.1 "$line"
    else
        echo "Error: Unable to find suitable command for network communication."
        exit 1
    fi
done < "$numbers_file"

# lastly delete the temp file
rm $numbers_file