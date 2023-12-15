"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import socket

def is_valid_port(port):
    return port >= 1024 and port <= 65535

def is_valid_domain(domain_name):
    # split the domain name by . to list
    domain_name_splited = domain_name.split(".")
    
    # initialise return value
    A = ""
    B = ""
    C = ""
    
    # get return value from list
    A = domain_name_splited[len(domain_name_splited)-1]
    if len(domain_name_splited) > 1:
        B = domain_name_splited[len(domain_name_splited)-2]
    if len(domain_name_splited) > 2:
        C = domain_name_splited[0:len(domain_name_splited)-2]
        C = ".".join(C)
    
    # check if domain name is valid
    # smart way to check https://stackoverflow.com/questions/47070472/how-to-check-in-python-that-a-string-contains-only-alphabets-and-hypen
    if A.replace('-','').isalnum() and (B == "" or B.replace('-','').isalnum()) and (C == "" or C.replace('-','').replace('.','').isalnum()):
        if (C == "") or (not C.startswith(".") and not C.endswith(".")):
            return True
    
    # return None if invalid
    return False

def main(args: list[str]) -> None:
    # Error handling: number of arguments
    if (len(args) != 1):
        print("INVALID ARGUMENTS")
        exit(1)
        
    # Error handling: can't open file
    try:
        config_file = open(args[0], "r")
    except:
        print("INVALID CONFIGURATION")
        exit(1)
        
    # Error handling: invalid server port number
    try:
        server_port = int(config_file.readline())
    except:
        print("INVALID CONFIGURATION")
        exit(1)
    if not is_valid_port(server_port):
        print("INVALID CONFIGURATION")
        exit(1)
    
    # domain name as key and port as value 
    # (since records contradict when they have the same 
    # (partial-)domain but different ports.)
    records = {}
        
    # Error handling: invalid record
    for line in config_file.readlines():
        splited = line.split(",")
        
        # there should not be comma in domain name, or missing port number
        if len(splited) != 2:
            print("INVALID CONFIGURATION")
            exit(1)
        
        # port should be number
        try:
            port = int(splited[1])
        except:
            print("INVALID CONFIGURATION")
            exit(1)
        
        # port need to be in the range [1024, 65535]
        if not is_valid_port(port):
            print("INVALID CONFIGURATION")
            exit(1)
            
        # domain need to be in correct format
        domain = splited[0]
        if not is_valid_domain(domain):
            print("INVALID CONFIGURATION")
            exit(1)
        
        # if the existed domain had different port then it's invalid
        if records.get(domain) != None and records.get(domain) != port:
            print("INVALID CONFIGURATION")
            exit(1)
        
        records[domain] = port
        
    config_file.close()
    
    # create socket to listen for incomming connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # specify type
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make address able to reuse without error
    server_socket.bind(("127.0.0.1", server_port)) # connect to address and port
    server_socket.listen()
    
    # initialise the buffer to collect message
    buffer = ""
    message = ""
    connection = None
    
    while True:
        
        # get message from incomming connection
        if message == "":
            connection, address = server_socket.accept()
            message = connection.recv(1024).decode() # max 1024 char
        
        # add each character to buffer until the newline
        while message:
            char = message[0]
            message = message[1:]
            buffer += char
            if char == "\n":
                break
        
        # check if buffer contains newline, if not then start listen again
        if buffer.find("\n") == -1:
            if message == "":
                connection.close()
            continue
        
        # otherwise execute the process depend on the buffer message
        if buffer.find("!") != -1:
            
            '''
                Accorded to the specs and faq sheet:
            "   The server should log INVALID\n if:
            The input cannot be interpreted as a complete command, 
            AND The input cannot be interpreted as a valid hostname.    "
                some of the edge case doesn't output INVALID\n such as
                - invalid port (will output INVALID PORT\n instead)
                - port already exist (will output INVALID PORT\n instead)
                - delete domain that's not exist (will output HOSTNAME NOT EXIST\n instead)
            '''
            
            # command check
            if buffer == "!EXIT\n":
                
                # exit the program
                exit(0)
            
            elif len(buffer) >= 5 and buffer[:5] == "!ADD ":
                
                # split to "!ADD,HOSTNAME,PORT" format
                splited = buffer.replace("\n", "").split(" ")
                
                # edge too many or not enough argument for ADD command
                if len(splited) != 3:
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID")
                    continue
                
                # edge when casting port value might not be number
                hostname = splited[1]
                try:
                    newport = int(splited[2])
                except ValueError:
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID PORT")
                    continue
                
                # edge host name is not valid domain name or partial domain name
                if not is_valid_domain(hostname):
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID")
                    continue
                
                # edge not valid port
                if not is_valid_port(newport):
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID PORT")
                    continue
                
                # edge port can't be the existed port in the records (unless it's the same hostname)
                port_is_exist = False
                for existed_port in records.values():
                    if newport == existed_port:
                        port_is_exist = True
                        break
                if port_is_exist and newport != records.get(hostname):
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID PORT")
                    continue
                        
                
                # add new port and hostname to record
                records[hostname] = newport
                
            elif len(buffer) >= 5 and buffer[:5] == "!DEL ":
                
                # split to "!DEL,HOSTNAME" format
                splited = buffer.replace("\n", "").split(" ")
                
                # edge too many or not enough argument for DEL command
                if len(splited) != 2:
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID")
                    continue
                
                hostname = splited[1]
                
                # edge host name is not valid domain name or partial domain name
                if not is_valid_domain(hostname):
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("INVALID")
                    continue
                
                # edge hostname is not the existed domain name in the records
                if records.get(hostname) == None:
                    buffer = "" # flush the buffer
                    if message == "":
                        connection.close()
                    print("HOSTNAME NOT EXIST")
                    continue
                
                # remove that hostname from the record
                records.pop(hostname)
                
            else:
                
                # other commands are invalid
                print("INVALID")
        
        else:
            
            # resolve the nameserver and send port back to recursor
            domain_name = buffer.replace("\n", "")
            dest_port = records.get(domain_name)
            
            if dest_port == None:
                dest_port = "NXDOMAIN"
                
            print(f"resolve {domain_name} to {dest_port}")
            connection.send((str(dest_port)+"\n").encode())
        
        # flush the buffer
        buffer = ""
        if message == "":
            connection.close()
    
    pass


if __name__ == "__main__":
    main(argv[1:])
