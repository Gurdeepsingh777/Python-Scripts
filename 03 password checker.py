class challenge:
    def pswd_checker(self,pswd):
        originalpswd="12341234"
        if pswd == originalpswd:            
            print("Successfull Login")
            return True
        else:
            print("Invalid Password!")
            return False

    def name_checker(self,nm):
        user="Gurdeep"
        if nm != user:
            print("Invalid Username!")
            return False
        else:
            print("User Name Found")
            return True

ob=challenge()
name=input("Enter Username:")


if ob.name_checker(name):
    paswd=input("Enter Password:")
    ob.pswd_checker(paswd)
