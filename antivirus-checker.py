import hashlib
import os
import shutil


VIRUS_DATABASE = ["5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"]


QUARANTINE_FOLDER = "virus_folder"


if not os.path.exists(QUARANTINE_FOLDER):
    os.makedirs(QUARANTINE_FOLDER)

def check_for_virus(file_path):
    
    try:
        
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()

        
        if file_hash in VIRUS_DATABASE:
            print(f"!!! VIRUS DETECTED !!! -> {file_path}")
            
            
            shutil.move(file_path, QUARANTINE_FOLDER)
            print(f"File moved to {QUARANTINE_FOLDER}")
    except:
        
        pass


path_to_scan = input("Scan karne ke liye folder ka path paste karein: ").strip('"')

print("Scanning shuru ho rahi hai...")

for root, dirs, files in os.walk(path_to_scan):
    for name in files:
       
        full_path = os.path.join(root, name)
        
        
        check_for_virus(full_path)

print("Scan poora hua!")
