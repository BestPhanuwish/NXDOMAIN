script_name=$(dirname "$0")
echo -e "\n[ Start testing module: $script_name (edge case) ]"

# go to the test dir
oldpwd=$(pwd)
cd $(dirname "$0")

# start a hard-coded server in background by coverage
coverage run --append $oldpwd/server.py one.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py zero.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py negative.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py edge_small.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py edge_large.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py letter.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py only_hostname.conf > actual.out
diff actual.out expect.out
coverage run --append $oldpwd/server.py multi.conf > actual.out
diff actual.out expect.out

# go back
cd $oldpwd