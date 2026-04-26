import hashlib

tohash=input("Whitch type of hash:")
file_path=input("Enter wordlist path:")
hashdata=input("Enter Hash Data:")

with open(file_path, 'r') as file:
    fileread=file.readlines()
    for line in fileread:
        if tohash == 'md5':
            hashobj=hashlib.md5(line.strip().encode()).hexdigest()
        elif tohash == 'sha1':
            hashobj=hashlib.sha1(line.strip().encode()).hexdigest()
        elif tohash == 'sha256':
            hashobj=hashlib.sha256(line.strip().encode()).hexdigest()
        elif tohash == 'sha512':
            hashobj=hashlib.sha512(line.strip().encode()).hexdigest()
        else:
            print("Invalid hash type")
            break
        if hashobj == hashdata:
            print(f"Password found: {line.strip()}")
            break
    else:
        print("Password not found")
    
    