script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name (edge case) ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py port_one.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py port_zero.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py port_negative.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py port_edge_small.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py port_edge_large.conf > actual.out
diff actual.out expect.out

# go back
cd $oldpwd