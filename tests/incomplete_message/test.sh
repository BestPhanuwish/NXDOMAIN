script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py sample.conf > actual.out &

# delay 2s to make sure the server is up and listening at port 1024
sleep 2

echo "fake recursor sends invalid command that's not complete"
printf "!FUM" | ncat 127.0.0.1 1024
printf "O\n" | ncat 127.0.0.1 1024

echo "fake recursor sends nameserver alphabettically"
printf "c" | ncat 127.0.0.1 1024
printf "o" | ncat 127.0.0.1 1024
printf "m" | ncat 127.0.0.1 1024
printf "\n" | ncat 127.0.0.1 1024

echo "fake recursor sends stacked ADD and DEL command"
printf "!ADD org 1026\norg\n!DE" | ncat 127.0.0.1 1024
sleep 1
printf "L org\norg\n" | ncat 127.0.0.1 1024

echo "fake recursor sends EXIT command with delay"
printf "!E" | ncat 127.0.0.1 1024
sleep 0.1
printf "XI" | ncat 127.0.0.1 1024
sleep 0.5
printf "T\n" | ncat 127.0.0.1 1024

# delay 0.1s
sleep 0.1

# compare the actual output and the expected output, but they are different!?
diff actual.out expect.out

# go back
cd $oldpwd