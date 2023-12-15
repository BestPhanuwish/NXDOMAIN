"""
Write code for your recursor here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import socket
from utils import is_valid_port, get_domain_format

def main(args: list[str]) -> None:
    # Error handling: number of arguments
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        exit(1)
    
    # get important variable
    root_port = int(args[0])
    timeout = float(args[1])
    
    # Error handling: root_port within range [1024, 65535]
    if not is_valid_port(root_port):
        print("INVALID ARGUMENTS") # I thought we need to output OSError..?
        exit(1)
    
    # loop get user input until EOF detected
    while True:
        try:
            domain_name = input()
        except EOFError:
            break
        
        # Get the domain name from C.B.A format in different variable
        A, B, C = get_domain_format(domain_name)
        
        # check if the domain name is valid
        if A is None:
            print("INVALID")
            continue
        
        try:
            # step 1: connect and send A to root server
            try:
                root_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify type
                root_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make address able to reuse without error
                root_server_socket.connect(("127.0.0.1", root_port))
            except:
                print("FAILED TO CONNECT TO ROOT")
                exit(1)
            root_server_socket.send((A+"\n").encode())
            root_server_socket.settimeout(timeout)
        
            # step 2: listen from root server to get TLD port number
            message = root_server_socket.recv(256).decode() # 256 char max
            if message == "NXDOMAIN\n":
                print("NXDOMAIN")
                continue
            tld_port = int(message)

            # step 3: connect and send B.A to tld port  
            try:
                tld_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify type
                tld_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make address able to reuse without error
                tld_socket.connect(("127.0.0.1", tld_port))
            except:
                print("FAILED TO CONNECT TO TLD")
                exit(1)
            tld_socket.send((B+"."+A+"\n").encode())
            tld_socket.settimeout(timeout)
            
            # step 4: listen from tld server to get authoritative port number
            message = tld_socket.recv(256).decode() # 256 char max
            if message == "NXDOMAIN\n":
                print("NXDOMAIN")
                continue
            authoritative_port = int(message)
            
            # step 5: connect and send C.B.A to authoritative port  
            try:
                authoritative_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify type
                authoritative_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make address able to reuse without error
                authoritative_socket.connect(("127.0.0.1", authoritative_port))
            except:
                print("FAILED TO CONNECT TO AUTH")
                exit(1)
            authoritative_socket.send((C+"."+B+"."+A+"\n").encode())
            authoritative_socket.settimeout(timeout)
            
            # step 6: listen from auth server to get main port number
            message = authoritative_socket.recv(256).decode() # 256 char max
            if message == "NXDOMAIN\n":
                print("NXDOMAIN")
                continue
            main_port = int(message)
            
            print(main_port)
            
        except TimeoutError:
            print("NXDOMAIN")
            continue
    
    pass


if __name__ == "__main__":
    main(argv[1:])
