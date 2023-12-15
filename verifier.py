"""
Write code for your verifier here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import pathlib
from utils import is_valid_port, is_valid_domain, is_valid_master_domain, get_domain_format

def main(args: list[str]) -> None:
    # Error handling: number of arguments
    if (len(args) != 2):
        print("invalid arguments")
        exit(1)
        
    # Error handling: can't open master file
    try:
        master_file = open(args[0], "r")
    except:
        print("invalid master")
        exit(1)
        
    # Error handling: invalid master port number
    try:
        master_port = int(master_file.readline())
    except:
        print("invalid master")
        exit(1)
    if not is_valid_port(master_port):
        print("invalid master")
        exit(1)
    
    # domain name as key and port as value 
    # (since records contradict when they have the same 
    # domain but different ports.)
    master_records = {}
        
    # Error handling: invalid record
    for line in master_file.readlines():
        splited = line.split(",")
        
        # there should not be comma in domain name, or missing port number
        if len(splited) != 2:
            print("invalid master")
            exit(1)
        
        # port should be number
        try:
            port = int(splited[1])
        except:
            print("invalid master")
            exit(1)
        
        # port need to be in the range [1024, 65535]
        if not is_valid_port(port):
            print("invalid master")
            exit(1)
            
        # domain need to be in correct format
        domain = splited[0]
        if not is_valid_master_domain(domain):
            print("invalid master")
            exit(1)
        
        # if the existed domain had different port then it's invalid
        if master_records.get(domain) != None and master_records.get(domain) != port:
            print("invalid master")
            exit(1)
        
        master_records[domain] = port
        
    master_file.close()


    # Error handling: if not a valid directory
    directory = pathlib.Path(args[1])
    if not directory.is_dir():
        print("singles io error")
        exit(1)
    pass

    # create a global map this will remember the root domain name and its port
    root_map = {}
    tld_map = {}

    # Loop through every single file in there (that's .conf file)
    all_single_records = {} # key: port, value: single records (dict)
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.name.endswith(".conf"):
            
            single_file = file_path.open("r")
            
            # Error handling: invalid port number
            try:
                root_port = int(single_file.readline())
            except:
                print("invalid single")
                exit(1)
            if not is_valid_port(root_port):
                print("invalid single")
                exit(1)
            
            # domain name as key and port as value
            single_records = {}
                
            # Error handling: invalid record
            for line in single_file.readlines():
                splited = line.split(",")
                
                # there should not be comma in domain name, or missing port number
                if len(splited) != 2:
                    print("invalid single")
                    exit(1)
                
                # port should be number
                try:
                    port = int(splited[1])
                except:
                    print("invalid single")
                    exit(1)
                
                # port need to be in the range [1024, 65535]
                if not is_valid_port(port):
                    print("invalid single")
                    exit(1)
                    
                # domain need to be in correct format
                domain = splited[0]
                if not is_valid_domain(domain):
                    print("invalid single")
                    exit(1)
                
                # if the existed domain had different port then it's invalid
                if single_records.get(domain) != None and single_records.get(domain) != port:
                    print("invalid single")
                    exit(1)
                
                single_records[domain] = port
                
            single_file.close()
            all_single_records[root_port] = single_records
            
            # loop through single records
            for single_domain, single_port in single_records.items():
                
                # check if domain in single is the same one as master
                if master_records.get(single_domain) != None:
                    # if there is check if the port is matched
                    if master_records.get(single_domain) != single_port:
                        # the port is not match then it's not equal
                        print("neq")
                        exit(0)
                else:
                    # otherwise check if it's partial domain of master domain
                    is_matched_domain = False
                    for master_domain in master_records.keys():
                        if master_domain.find(single_domain) != -1:
                            is_matched_domain = True
                            break
                    if not is_matched_domain:
                        print("neq")
                        exit(0)
                
                # if it's the root nameserver then remember its port
                A, B, C = get_domain_format(single_domain, True)
                if B == "":
                    root_map[single_domain] = single_port
                elif C == "":
                    tld_map[single_domain] = single_port
    
    # loop through every single records and check if the port is match
    for port, single_records in all_single_records.items():
        for single_domain in single_records.keys():
            
            # check whether the record is root or tld or auth nameserver
            A, B, C = get_domain_format(single_domain, True)
            if B == "":
                # if it's root nameserver record then this is root.conf
                # hence it can have any port doesn't really matter
                continue
            elif C == "":
                # if it's tld nameserver record then this is tld.conf
                # the port need to match the root port for this to be legit
                if port != root_map.get(A):
                    print("neq")
                    exit(0)
            else:
                # if it's auth nameserver record then this is auth.conf
                # the port need to match the tld port for this to be legit
                if port != tld_map.get(f"{B}.{A}"):
                    print("neq")
                    exit(0)
    
    # if there's no exit when verifying, that's mean they are equal
    print("eq")
    exit(0)


if __name__ == "__main__":
    main(argv[1:])