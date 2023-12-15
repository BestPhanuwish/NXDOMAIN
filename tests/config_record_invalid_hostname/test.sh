script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name (edge case) ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py weird_char.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py C_contain_dot.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py only_port.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py multi.conf > actual.out
diff actual.out expect.out

# go back
cd $oldpwd