import itertools
import string
import time

def bfcrack(paswd):
    chars = string.ascii_lowercase + string.digits
    attempts = 0
    start_time = time.time()

    print("Starting brute-force attack...")

    for length in range(1,8):
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess_str = ''.join(guess)
            if guess_str == paswd:
                end_time = time.time()
                print(f"Password found: {guess_str}")
                print(f"Attempts: {attempts}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return
    print("Password not found.")

if __name__ == "__main__":
    password = input("Enter the password to crack: ")
    bfcrack(password)