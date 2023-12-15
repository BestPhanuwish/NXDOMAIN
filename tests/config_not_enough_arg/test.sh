script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name (edge case) ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py > actual.out

# compare the actual output and the expected output, but they are different!?
diff actual.out expect.out

# go back
cd $oldpwd