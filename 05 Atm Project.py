class Atm:
    def pin_checker(self,pin):
        oripin='7733'
        if pin==oripin:
            return True
        else:
            print("Wrong Pin..!")
            return False
    def user_checker(self,user):
        oriuser='Gurdeep'
        if user==oriuser:
            return True
        else:
            print("Invalid username")
            return False

class Bank_Info:
    def __init__(self,balance):
        self.__amount=balance
        self.history=[]

    def check_balance(self):
        print("Current balance:",self.__amount)

    def deposit(self,amount):
        if amount>0:
            self.__amount+=amount
            self.history.append(f"Deposit: {amount}")
            print("Deposited Amount")
        else:
            print("Invalid Amount")

    def withdraw(self,amount):
        if amount<=self.__amount:
            self.__amount-=amount
            self.history.append(f"withdraw: {amount}")
            print("\n---Successfully Withdraw Amount---")
        else:
            print("Insufficent Balance")
            return False
    def show_history(self):
        print("\n---------Transaction History------")
        for h in self.history:
            print(h)

obj=Atm()
ob=Bank_Info(700)
nm=input("Enter Username:")
if obj.user_checker(nm):
    atmpt=0
    while atmpt<3:
        pin=input("Enter Pin Number:")
        if obj.pin_checker(pin):
            break
        atmpt+=1
    if atmpt==3:
        print("Card Blocked")
        exit()
    while True:
        print("\n1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. History")
        print("5. Exit")

        choice=input("Choose: ")
        if choice=="1":
            ob.check_balance()

        elif choice=='2':
            amt=int(input("Enter Amount:"))
            ob.deposit(amt)

        elif choice=='3':
            amt=int(input("Enter Amount:"))
            ob.withdraw(amt)

        elif choice=='4':
            ob.show_history()
                
        elif choice=='5':
            print("Thank you")
            break
        else:
            print("invalid")
