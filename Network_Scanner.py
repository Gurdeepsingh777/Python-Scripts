import threading
import socket
import time


target = input("Enter the target IP address: ")
startp=int(input("Enter the starting port number: "))
endp=int(input("Enter the ending port number: "))

start_time = time.time()
open_ports = []
lock = threading.Lock()

# thread worker that scans a single port and records result

def scan_port(port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            # acquire lock before printing/appending to shared list
            with lock:
                print(f"Port {port} is open")
                open_ports.append(port)
    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass

threads = []
for port in range(startp, endp + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

# wait for all threads to finish
for t in threads:
    t.join()

end_time = time.time()
total_time = end_time - start_time

with open("scan_results.txt", "w") as f:
    f.write(f"Target: {target}:\n")
    f.write(f"Open ports: {open_ports}\n")
    f.write(f"Total scan time: {total_time} seconds\n")