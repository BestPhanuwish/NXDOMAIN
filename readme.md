# NXDOMAIN

## Description

NXDOMAIN is a program written in Python to simulate how DNS infrastructure works within local machine. This program involve 4 different main python file.

1. recursor.py by implement simulation of DNS recursor program use to resolve the hostname by queries a DNS nameserver from the root send through port and recieve the respond from TLD nameserver, do the same until get the  authoritative nameserver and print out the last port connect to it.
2. server.py by implement simulation of DNS server program that first gather the nameserver and its port in the config file and then wait for message to resolve the nameserver and feed the port back to recursor. It also recieve external command like !ADD, !DEL, and !EXIT (will explain on "How to run" section)
3. launcher.py by Implement the launcher program that generates DNS server configurations from master configuration file that contains many hostname that's not partial hostname.
4. verifier.py by Implement the verifier program that validates the equivalency of configuration files to ensure that the port and hostname are coherent.

## About

NXDOMAIN program is dedicated for educational purpose only. Since this is only a part for university project at USYD - INFO1112 Computing 1B OS and Network Platforms given by the task:
> You are going to implement a simplified DNS infrastructure that contains a DNS recursor, some DNS servers, a launcher program that generates configurations for the DNS servers and a verifier that validates the configurations of the DNS servers. When the DNS servers are running, any end user can ask the recursor to resolve a hostname. Then, the recursor initiates a chain of DNS queries to the DNS servers via TCP connection. Eventually, the recursor shall collect responses from the DNS servers, and resolve the hostname to a valid identifier or NXDOMAIN to the end user. - USYD

Only student at USYD can see the [scaffold](https://github.sydney.edu.au/tmai6782/2023-INFO1112-A2/blob/main/NXDOMAIN.md)

## Goals and Knowledge outcome

During the development of NEXDOMAIN program I had gain an understanding of
- DNS (Domain Name System) infrastructure concept
- Python file handler and socket programming
- Shell scripting communicate between client and server from local host
- Black-box testing to gain code coverage

## System Requirement

Linux\
Architecture: ARM64 (aarch64)\
Machine: QEMU 7.2 ARM Virtual Machine (alias of virt-7.2)\
Network: Emulated VLAN

## How to run

### 1. Create master configuration file and directory for single configurations

Create file name "master.conf".\
Inside the master.conf type in a root port followed by many hostname and its port in form of "hostname,portNum". Or simply just copy paste the template below:

> 1024\
<span>www.google.com,1029</span>\
docs.google.com,1030\
account.google.com,1031\
en.wikipedia.org,1032\
fr.wikipedia.org,1033\
zh.wikipedia.org,1034\
ar.wikipedia.org,1035

Then for the directory of the single configuration you can simply create a folder name "single-config"

### 2. launcher.py to generate single configurations

After the first step. Then you can run the launcher by type command in root repo\
```
python3 launcher.py master.conf single-config
```
This will generate single configurations in that folder

### 3. verifier.py to check if single configurations are generate correctly

After you had generate the single configurations on specific directory.\
You can check if all that are coordinate with master configuration.\
This is useful in case you've create single configuration file that doesn't coherent to the other sigle configurations or doesn't match the master configuration.
You can run the verifier by type in command line in terminal at root repo:
```
python3 verifier.py master.conf single-config
```
If it's output "eq" that mean it had been correctly set up.\
If it's output "neq" that mean they are not match.\

### 4. server.py set up the server to simulate its behaviour

To simulate the work of server.py, we can either use single configuration that we had generate from previous step or create a new single configuration file.\
**HOWEVER**, from step 4 only we will create a new single configuration file named "single.conf" in the root of the repo.\
Use the template below or think of one yourself (single configuration file allow partial-domain name)

> 1025\
com,1234\
org,2587\
<span>www.google.com,8987</span>\
google.com,8888

After setup the single configuration file then we can run the command in the terminal
```
python3 server.py single.conf &
```
> *By including '&' symbol we run the server.py in the background so that we can send message to server while it's still running in the same terminal*

Now, the fun part is that we can pretend to be recursor by sending hostname to server and the server can logout the port number on terminal.\
Try sending the message to the server using template:
```
echo 'hostname' | nc 127.0.0.1 [root port number]
```
Or if you follow along and use the same single config file then just run
```
echo 'com' | nc 127.0.0.1 1025
```
> *Note: we send the message using local host 127.0.0.1. And 'nc' command can be replace by 'ncat' or './netcat' if they're available*

You'll see that it will print out the port number of respective hostname which in this case 'com' had port 1234.\
If the hostname is not exist, then it will resolve to NXDOMAIN.

The server can also receive external message such as

**ADD command**
template:
```
echo '!ADD HOSTNAME PORT' | nc 127.0.0.1 [root port number]
```
Try
```
echo '!ADD au 1666' | nc 127.0.0.1 1025
```
This will temporary add hostname 'au' with port '1666' to the server records. You can test if they had been add by run the command:
```
echo 'au' | nc 127.0.0.1 1025
```
This will logout the port 1666 to terminal.

**DEL command**
template:
```
echo '!DEL HOSTNAME' | nc 127.0.0.1 [root port number]
```
Try
```
echo '!DEL au' | nc 127.0.0.1 1025
```
This will temporary delete the hostname 'au' from the server records. You can test if the hostname still exist by run the command:
```
echo 'au' | nc 127.0.0.1 1025
```
This will logout resolve to NXDOMAIN to the terminal.

**EXIT command**
Try
```
echo '!EXIT' | nc 127.0.0.1 1025
```
This will shutdown the running server.

### 5. recursor.py resolve domain name by communicate with different nameservers

Assume you had the same 'single-config' folder after you launch in step 2.\
Then you can run all the server using data inside 'single-config' folder at once.\
I've create a shell script include in this repo called 'run_all_singles.sh'. That will run all the server by loop all the single config file and run the server on it. You can simply run this command in the terminal for this step:
```
bash run_all_singles.sh single-config
```
This will log out which server had been up and running currently

Next, we can start our recursor.py program that acts as an resolver.\
Its job is to resolve domain name by divide up the hostname and send it to root server to resolve, then respond with port coordinate to tld server, then the recursor will send the message using the port that it got to tld server, do the same to authoritative server. Until it log out the port coordinate to domain name that we input.\
To run the recursor.py program using the template below:
```
python3 recursor.py [root port] [timeout]
```
> To get a [root port], you need to go in the 'single-config' folder. Then find the file named 'root.conf'. Look at the number on the TOP of that file, there you are root port.
> \[timeout] is maximum number of time it takes to wait for server to respond. In reality, to communicate to server takes a lot of time and if it's taking too long then we can terminate the request.

After recursor.py program had start. You can start typing in the domain on stdin in terminal. Look up the domain name available on 'master.conf' or simply type in the example:
```
www.google.com
```
The program will start communicate with different nameserver and end up output the port number that you seen in 'master.conf'

To close the recursor program simply use hotkey `Ctrl-D`

If the domain name that you type in is unavailable or is a patial-domain name. Then it will output 'INVALID'.

To shut down all the running server simply run
```
bash close_all_singles.sh
```
> *Note: This must be run only when you had execute command run_all_singles before*

## How to test the program

Simply just type "bash tests/run.sh" on the root of the git repo.
This will generate coverage report after all the testings are done.\
*Note: The testing suite only test server.py and is a black-box testing

## Contributor

USYD: https://www.sydney.edu.au/

## Credit

Programmer: Best Phanuwish