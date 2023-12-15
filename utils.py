import random


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

def get_domain_format(domain_name, can_be_partial=False):
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
        
    if can_be_partial:
        if A.replace('-','').isalnum() and (B == "" or B.replace('-','').isalnum()) and (C == "" or C.replace('-','').replace('.','').isalnum()):
            if (C == "") or (not C.startswith(".") and not C.endswith(".")):
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