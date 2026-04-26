import os


class Student:
    def name_input(self,name):
        self.name=name
        print("Student Name:",self.name)
    
    def marks_input(self):
        self.maths=int(input("Maths:"))
        self.physics=int(input("Physics:"))
        self.chemistry=int(input("Chemistry:"))
        self.total=self.maths+self.physics+self.chemistry
        print("Total Marks:",self.total)
        
    def percentage(self):
        self.percentage=(self.total/300)*100
        print("Percentage:",self.percentage)

    def result(self):
        if self.percentage>=90:
            print("Grade A")
        elif self.percentage>=75 and self.percentage<90:
            print("Grade B")
        elif self.percentage>=50 and self.percentage<75:
            print("Grade C")
        else:
            print("Fail")
    def display(self):
        print("Student Name:",self.name)
        print("Maths:",self.maths)
        print("Physics:",self.physics)
        print("Chemistry:",self.chemistry)
        print("Total Marks:",self.total)
        print("Percentage:",self.percentage)

    def store_data(self):
        record = {
            'name': self.name,
            'maths': self.maths,
            'physics': self.physics,
            'chemistry': self.chemistry,
            'total': self.total,
            'percentage': self.percentage
        }
        file=open("student.txt",'a')
        file.write(f"\n{record}")
        file.close()
        #save_student_record(record)
        print('Saved student record for:', self.name)

def add_student_interactive():
    obj = Student()
    name_input = input("Enter Student Name:")
    obj.name_input(name_input)
    print("---Enter All Subject Marks---")
    obj.marks_input()
    obj.percentage()
    obj.display()
    obj.result()
    obj.store_data()


def view_records():
    #records = load_student_records()
    record=open("student.txt",'r')
    content=record.read()
    if not content:
        print('No saved student records found.')
        return
    print('\nSaved Student Records:')
    print(content)
    record.close()


def main():
    while True:
        print('\n--- Student Records Menu ---')
        print('1. Add new student')
        print('2. View all saved records')
        print('3. Exit')
        choice = input('Choose an option (1/2/3): ').strip()
        if choice == '1':
            add_student_interactive()
        elif choice == '2':
            view_records()
        elif choice == '3':
            print('Exiting. Goodbye!')
            break

        else:
            print('Invalid choice, please enter 1, 2, or 3.')


if __name__ == '__main__':
    main()
