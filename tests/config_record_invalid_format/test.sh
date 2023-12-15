script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name (edge case: not in the spec) ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py too_few_arg.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py too_many_arg.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py misplace.conf > actual.out
diff actual.out expect.out

# go back
cd $oldpwd