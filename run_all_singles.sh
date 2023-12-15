#!/bin/bash

directory=$1
rootports_file="root_port_temp.txt"

if [ -z "$directory" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' not found."
    exit 1
fi

# Close all the server running if user forget to close it
if [ -f "root_port_temp.txt" ]; then
    bash close_all_singles.sh
fi

for file in "$directory"/*.conf; do
    filename=$(basename "$file")
    if [ "$filename" != "master.conf" ]; then
        echo "Run server on $filename"
        python3 server.py "$file" &

        # Read the number from the first line of the file
        number=$(head -n 1 "$file")
        
        # Append the number to the numbers file
        if [ -n "$number" ]; then
            echo "$number" >> "$rootports_file"
        fi
    else
        echo "Ignoring master.conf"
    fi
done
