"""
Write code for your launcher here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import pathlib
import random

def is_valid_port(port):
    return port >= 1024 and port <= 65535

def is_valid_master_domain(domain_name):
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
        
    # Domain name can't be partial
    if A == "" or B == "" or C == "":
        return False
    
    # check if domain name is valid
    # smart way to check https://stackoverflow.com/questions/47070472/how-to-check-in-python-that-a-string-contains-only-alphabets-and-hypen
    if A.replace('-','').isalnum() and (B.replace('-','').isalnum()) and (C.replace('-','').replace('.','').isalnum()):
        if (C == "") or (not C.startswith(".") and not C.endswith(".")):
            return True
    
    # return None if invalid
    return False

def get_domain_format(domain_name):
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
    if A.replace('-','').isalnum() and (B != "" and B.replace('-','').isalnum()) and (C != "" and C.replace('-','').replace('.','').isalnum()):
        if (C != "") and (not C.startswith(".") and not C.endswith(".")):
            return A, B, C
    
    # return None if invalid
    return None, None, None

# get random number of port that's not exist within records yet
def get_random_port(records) -> int:
    count = 0
    while count < 64512:
        # Generate a random number between 1024 and 65535
        random_port = random.randint(1024, 65535)

        # Check if the random_port is not in the values of the "records" dictionary
        if random_port not in records.values():
            return random_port
        
    print("Error: Number of port is not enough")
    exit(1)

def main(args: list[str]) -> None:
    # Error handling: number of arguments
    if (len(args) != 2):
        print("INVALID ARGUMENTS")
        exit(1)
        
    # Error handling: can't open master file
    try:
        master_file = open(args[0], "r")
    except:
        print("INVALID MASTER")
        exit(1)
        
    # Error handling: invalid master port number
    try:
        master_port = int(master_file.readline())
    except:
        print("INVALID MASTER")
        exit(1)
    if not is_valid_port(master_port):
        print("INVALID MASTER")
        exit(1)
    
    # domain name as key and port as value 
    # (since records contradict when they have the same 
    # domain but different ports.)
    records = {}
        
    # Error handling: invalid record
    for line in master_file.readlines():
        splited = line.split(",")
        
        # there should not be comma in domain name, or missing port number
        if len(splited) != 2:
            print("INVALID MASTER")
            exit(1)
        
        # port should be number
        try:
            port = int(splited[1])
        except:
            print("INVALID MASTER")
            exit(1)
        
        # port need to be in the range [1024, 65535]
        if not is_valid_port(port):
            print("INVALID MASTER")
            exit(1)
            
        # domain need to be in correct format
        domain = splited[0]
        if not is_valid_master_domain(domain):
            print("INVALID MASTER")
            exit(1)
        
        # if the existed domain had different port then it's invalid
        if records.get(domain) != None and records.get(domain) != port:
            print("INVALID MASTER")
            exit(1)
        
        records[domain] = port
        
    master_file.close()


    # Error handling: if not a valid directory
    directory = pathlib.Path(args[1])
    if not directory.is_dir():
        print("NON-WRITABLE SINGLE DIR")
        exit(1)

    # Create a Path object for open file
    root_path = directory/"root.conf"
    root_file = root_path.open('w')
        
    # give random port to root
    root_file.write(f"{get_random_port(records)}\n")
    
    # create a map to map the parent nameserver with its child file
    tld_map = {}
    auth_map = {}
    
    # put information from records to single files
    for domain, port in records.copy().items():
        A, B, C = get_domain_format(domain)
        
        # create root-nameserver and generate port (if not exist)
        # and create new tld file respect to the new root
        if records.get(A) == None:
            newPort = get_random_port(records)
            records[A] = newPort
            root_file.write(f"{A},{newPort}\n")
            
            # create new tld file and add port then map it
            tld_path = directory/f"tld-{A}.conf"
            tld_file = tld_path.open("w")
            tld_file.write(f"{newPort}\n")
            
            # map the root nameserver with tld file 
            # to access it later if they had the same root nameserver
            tld_map[A] = tld_file
            
        # create tld nameserver and generate port (if not exist)
        if records.get(f"{B}.{A}") == None:
            # ensure that tld file is match and exist before write on it
            tld_file = tld_map.get(A)
            
            newPort = get_random_port(records)
            records[f"{B}.{A}"] = newPort
            tld_file.write(f"{B}.{A},{newPort}\n")
            
            # create new auth file and add port then map it
            auth_path = directory/f"auth-{B}.conf"
            auth_file = auth_path.open("w")
            auth_file.write(f"{newPort}\n")
            
            # map the root nameserver with tld file 
            # to access it later if they had the same tld nameserver
            auth_map[f"{B}.{A}"] = auth_file
        
        # ensure that auth file is match and exist before write on it
        auth_file = auth_map.get(f"{B}.{A}")
        
        # add nameserver from master to auth automatically
        auth_file.write(f"{domain},{port}\n")
    
    # close all the single file after done writing
    root_file.close()
    for tld_file in tld_map.values():
        tld_file.close()
    for auth_file in auth_map.values():
        auth_file.close()
    
    pass


if __name__ == "__main__":
    main(argv[1:])
