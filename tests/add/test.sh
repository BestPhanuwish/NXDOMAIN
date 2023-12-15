script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py sample.conf > actual.out &

# delay 2s to make sure the server is up and listening at port 1024
sleep 2

echo "fake recursor sends ADD command over TCP and then send newly added nameserver for it to resolve"
while IFS= read -r line; do
    echo $line | ncat 127.0.0.1 1024
    sleep 0.1
done < input.in

# compare the actual output and the expected output, but they are different!?
diff actual.out expect.out

# go back
cd $oldpwd